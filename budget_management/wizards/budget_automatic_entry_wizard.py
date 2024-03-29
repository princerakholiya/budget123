from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class AutomaticEntryWizard(models.TransientModel):
    _name = "budget.automatic.entry.wizard"
    _description = "Create Automatic Entries"

    date_from = fields.Date("Start Date")
    date_to = fields.Date("End Date")
    periods = fields.Selection(
        [
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
        ],
        default="monthly",
        required=True,
    )
    # analytic_plans = fields.Many2many("account.analytic.plan")
    
    def _get_months_in_range(self, date_from, date_to):
        months_in_range = []
        current_month = date_from.replace(day=1)
        while current_month <= date_to:
            months_in_range.append(current_month)
            current_month += relativedelta(months=1)
        return months_in_range

    def do_action(self):
        if self.periods == "monthly":
            for month in self._get_months_in_range(self.date_from, self.date_to):
                self.env['budget.budget'].create({
                    'date_from': month.replace(day=1),
                    'date_to': (month + relativedelta(months=1)).replace(day=1),  # Use relativedelta to get the next month
                    'name': month.strftime('%B %Y'),  # Add month and year as the name
                })
        
    
    
    