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
        # Odoo calcule la valeur une fois, l'écrit "en dur" dans la base de données,
        # et ne la modifie que si les données sources changent
        store=True,
        help='Average score calculated from all associated questions.'
    )

    questions_count = fields.Integer(
        string='Question Count',
        compute='_compute_stats', # Utilise la même méthode combinée
        store=True,
        help='Number of questions associated with this feedback.'
    )

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
    # AVANT insértion ou mise à jour en base de données.
    @api.constrains('state', 'questions_ids')
    def _check_questions_before_done(self):
        for record in self:
            if record.state == 'done' and not record.questions_ids:
                # Le message d'erreur doit être en anglais pour l'utilisateur final
                raise ValidationError("You cannot validate the feedback if there are no associated questions!")