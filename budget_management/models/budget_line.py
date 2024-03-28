from odoo import fields, models



class BudgetLine(models.Model):
    _name = "budget.line"
    _description = "Budget"

    _name = "budget.line"
    _description = "Budget Line"

    name = fields.Char()
    crossovered_budget_id = fields.Many2one('budget.budget', 'Budget', ondelete='cascade', index=True, required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    
    planned_amount = fields.Float(
        'Planned Amount', required=True,
        help="Amount you plan to earn/spend. Record a positive amount if it is a revenue and a negative amount if it is a cost.")
    practical_amount = fields.Float(string='Practical Amount', help="Amount really earned/spent.")
    
    
    