from odoo import models, fields, api

class HrApplicant(models.Model):  

    # Au lieu de créer une nouvelle table dans la base de données, 
    # Odoo va chercher le modèle existant hr.applicant
    _inherit = 'hr.applicant'

    # Champ calculé pour afficher le nombre dans le bouton
    feedback_count = fields.Integer(
        string='Feedback Count', 
        compute='_compute_feedback_count'
    )

    def _compute_feedback_count(self):
        for record in self:
            # On compte le nombre de feedbacks liés à cette candidature
            record.feedback_count = self.env['hr.feedback'].search_count(
                [('application_id', '=', record.id)]
            )

    def action_view_feedbacks(self):
        """
        Cette méthode est appelée quand on clique sur le Smart Button.
        Elle renvoie une action vers la vue liste des feedbacks.
        """
        self.ensure_one()  # vérifie que self ne contient qu'une seule candidature, pour pas appeler details sur plusieurs candidatures

        return {
            'name': 'Feedbacks',
            'type': 'ir.actions.act_window', #ouvre une nouvelle fenêtre action
            'res_model': 'hr.feedback',
            'view_mode': 'list,form', 
            'domain': [('application_id', '=', self.id)], # Filtre pour ne voir que ceux du candidat
            'context': {'default_application_id': self.id}, # Pré-remplit le candidat si on crée un nouveau feedback
        }