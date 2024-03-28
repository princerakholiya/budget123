/** @odoo-module **/
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { registry } from "@web/core/registry";

const { Component } = owl;
const cogMenuRegistry = registry.category("cogMenu");

export class CogMenu extends Component {
    async actionNewOption() {
        var currentModel = this.env.searchModel.resModel;
        console.log(currentModel);
        // Include your action for the menu here...
    }
}

CogMenu.template = "blog_cog_menu.NewOption";
CogMenu.components = { DropdownItem };

export const CogMenuItem = {
    Component: CogMenu,
    groupNumber: 20,
    isDisplayed: ({ config }) => config.viewType != "kanban",
};

cogMenuRegistry.add("new-option", CogMenuItem, { sequence: 10 });
