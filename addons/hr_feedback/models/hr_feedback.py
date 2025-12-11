from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HrFeedback(models.Model):
    _name = 'hr.feedback'
    _description = 'Candidate Interview Feedback'
    _rec_name = 'application_id' # Affiche nom au lieu de id

    author_id = fields.Many2one(
        'res.users',
        string='Author',
        required=True,
        default=lambda self: self.env.user,
        help='The user who created the feedback.'
    )

    description = fields.Text(
        string='Description',
        help='Detailed description of the feedback.'
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ], string='Status', default='draft', required=True)

    # --- NOUVEAUTÉ : L'AMÉLIORATION "Questions Types" ---
    interview_type = fields.Selection([
        ('hr', 'Ressources Humaines'),
        ('tech', 'Technique'),
        ('manager', 'Management')
    ], string="Type d'entretien", help="Sélectionnez un type pour pré-remplir les questions.")
    # ----------------------------------------------------

    # Many (feedbacks) to One (application).
    application_id = fields.Many2one(
        'hr.applicant',
        string='Related Application',
        required=True,
        ondelete='cascade', # Si on supprime la candidature, on supprime les feedbacks associés
        help='The job application associated with this feedback.'
    )

    questions_ids = fields.One2many(
        'hr.feedback.question', # Nom du modèle cible à récupérer
        'feedback_id',          # Le nom exact du champ Many2one inverse dans le modèle cible
        string='Questions',
        help='List of questions associated with this feedback.'
    )

    average_score = fields.Float(
        string='Average Score',
        compute='_compute_stats', # Utilise la méthode combinée ci-dessous
        store=True,
        help='Average score calculated from all associated questions.'
    )

    questions_count = fields.Integer(
        string='Question Count',
        compute='_compute_stats', # Utilise la même méthode combinée
        store=True,
        help='Number of questions associated with this feedback.'
    )

    # LOGIQUE DE L'AMÉLIORATION (@api.onchange)
    @api.onchange('interview_type')
    def _onchange_interview_type(self):
        """
        Génère automatiquement des questions quand on change le type d'entretien.
        """
        if not self.interview_type:
            return

        # 1. Définir les questions selon le type
        questions_data = []
        if self.interview_type == 'hr':
            questions_data = [
                'Pourquoi voulez-vous quitter votre poste actuel ?',
                'Quelles sont vos prétentions salariales ?',
                'Où vous voyez-vous dans 5 ans ?'
            ]
        elif self.interview_type == 'tech':
            questions_data = [
                'Quelle est votre expérience avec Python/Django ?',
                'Expliquez le concept de l\'ORM Odoo.',
                'Comment gérez-vous les conflits Git ?',
                'Avez-vous déjà utilisé Docker ?'
            ]
        elif self.interview_type == 'manager':
            questions_data = [
                'Comment gérez-vous le stress ?',
                'Racontez une situation de conflit résolue.',
                'Préférez-vous travailler seul ou en équipe ?'
            ]

        # 2. Préparer la commande pour mettre à jour le One2many
        # (5, 0, 0) : Supprime toutes les lignes existantes (nettoyage)
        lines = [(5, 0, 0)]
        
        for q in questions_data:
            # (0, 0, values) : Crée une nouvelle ligne
            lines.append((0, 0, {
                'label': q,
                'score': 0, # Score par défaut
            }))

        # 3. Appliquer les changements
        self.questions_ids = lines
    # -----------------------------------------------------

    # permet de recalculer un champ automatiquement quand un autre change.
    @api.depends('questions_ids', 'questions_ids.score')
    def _compute_stats(self):
        """
        Calcule à la fois le nombre de questions et le score moyen
        pour optimiser les performances.
        """
        for record in self:
            # 1. Calcul du nombre de questions
            record.questions_count = len(record.questions_ids)
            
            # 2. Calcul de la moyenne
            if record.questions_count > 0:
                total_score = sum(q.score for q in record.questions_ids)
                record.average_score = total_score / record.questions_count
            else:
                record.average_score = 0.0

    # Il sert à bloquer l'enregistrement si une règle n'est pas respectée.
    @api.constrains('state', 'questions_ids')
    def _check_questions_before_done(self):
        for record in self:
            if record.state == 'done' and not record.questions_ids:
                # Le message d'erreur doit être en anglais pour l'utilisateur final
                raise ValidationError("You cannot validate the feedback if there are no associated questions!")