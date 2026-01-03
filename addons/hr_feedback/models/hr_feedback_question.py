from odoo import models, fields

# table qui doit être créée dans la base de données PostgreSQL
class HrFeedbackQuestion(models.Model):
    _name = 'hr.feedback.question'
    _description = 'Question du Feedback'
    # pas de champ 'name', utilise le contenu du champ 'label' pour afficher le nom
    _rec_name = 'label'

    # Texte de la question
    label = fields.Char(string='Question', required=True)

    # Réponse donnée par le candidat
    answer = fields.Text(string='Réponse du candidat')

    # Note attribuée (Float pour permettre des demi-points)
    score = fields.Float(string='Score /10', default=0.0)

    # Lien inverse vers le Feedback
    feedback_id = fields.Many2one(
        'hr.feedback', 
        string='Feedback associé', 
        ondelete='cascade' # Si on supprime le feedback, on supprime les questions
    )

    # Lien vers une compétence (nécessite le module hr_skills)
    skill_id = fields.Many2one('hr.skill', string='Compétence évaluée')