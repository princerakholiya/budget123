from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class BudgetBudget(models.Model):
    _name = "budget.budget"
    _description = "Budget"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Budget Name", required=True)
    user_id = fields.Many2one(
        "res.users", "Responsible", default=lambda self: self.env.user
    )
    date_from = fields.Date("Start Date")
    date_to = fields.Date("End Date")
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
            ("revised", "Revised"),
            ("done", "Done"),
            
        ],
        "Status",
        default="draft",
        index=True,
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
    )
    # crossovered_budget_line = fields.One2many('crossovered.budget.lines', 'crossovered_budget_id', 'Budget Lines', copy=True)
    company_id = fields.Many2one(
        "res.company", "Company", required=True, default=lambda self: self.env.company
    )
    
    color = fields.Integer("Color")
    budget_line_ids = fields.One2many("budget.line", "crossovered_budget_id")
    on_over_budget = fields.Selection(
        [
            ("warning", "Warning"),
            ("restriction", "Restriction"), 
        ],
        "On over budget",
        
    )

    def action_budget_confirm(self):
        self.write({"state": "confirm"})

    def action_budget_draft(self):
        self.write({"state": "draft"})

    def action_budget_validate(self):
        self.write({"state": "validate"})

    def action_budget_cancel(self):
        self.write({"state": "cancel"})

    def action_budget_done(self):
        self.write({"state": "done"})

    def action_view_configuration(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Configuration budget",
            "res_model": "budget.budget",
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_view_budget_line(self):
        budget_line_ids = self.budget_line_ids.ids
        action = {  
            "type": "ir.actions.act_window",
            "name": "Budget line",
            "res_model": "budget.line",
            "view_mode": "tree,pivot,gantt",
            "target": "current",
            "domain": [("id", "in", budget_line_ids)],
        }
        return action
    
    revised_id = fields.Many2one('budget.budget', string='Revised Budget Id', readonly=True)
    child_budget_id = fields.One2many('budget.budget','revised_id', string='Parent Budget ID',readonly=True)

    def action_budget_revise(self):
        new_budget = self.copy({
            "state": "draft",
            "revised_id": self.id,
        })
        self.child_budget_id=new_budget
        return {
            "type": "ir.actions.act_window",
            "name": "Revised Budget",
            "res_model": "budget.budget",
            "res_id": new_budget.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_budget_confirm(self):
        self.revised_id.state="revised"
        self.write({"state": "confirm"})
        
    

    