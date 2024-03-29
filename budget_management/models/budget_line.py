from odoo import fields, models, api



class BudgetLine(models.Model):
    _name = "budget.line"
    _description = "Budget"

    _name = "budget.line"
    _description = "Budget Line"

    name = fields.Char()
    crossovered_budget_id = fields.Many2one('budget.budget', 'Budget', ondelete='cascade', index=True, required=True)
    date_to = fields.Date(related="crossovered_budget_id.date_to")
    date_from = fields.Date(related="crossovered_budget_id.date_from")
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    user_id = fields.Many2one(
        "res.users", default=lambda self: self.env.user
    )
    planned_amount = fields.Float(
        'Budget Amount', required=True,
        help="Amount you plan to earn/spend. Record a positive amount if it is a revenue and a negative amount if it is a cost.")
    practical_amount = fields.Float(string='Achieved Amount', help="Amount really earned/spent.")
    percentage = fields.Float(string = 'Percentage', compute="_compute_percentage")
    
    @api.depends('planned_amount', 'practical_amount')
    def _compute_percentage(self):
        for line in self:
            line.percentage = (line.practical_amount / line.planned_amount) * 100 if line.planned_amount!= 0 else 0.0
    

    @api.onchange('planned_amount', 'practical_amount')
    def _onchange_planned_amount(self):
        for line in self:
            if line.practical_amount > line.planned_amount:
                if line.crossovered_budget_id.on_over_budget == 'warning':
                    return {'warning': {
                        'title': 'Over Budget',
                        'message': 'The practical amount for this budget line is higher than the planned amount. '
                                   'Do you want to continue anyway?'
                    }}
                    
    @api.depends('analytic_account_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.analytic_account_id.name
    
    
    