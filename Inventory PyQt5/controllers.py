from PyQt5.QtWidgets import QMessageBox
from models import InventoryModel
from ui_main import InventoryApp


class InventoryController:
    def __init__(self, ui: InventoryApp):
        self.ui = ui
        self.model = InventoryModel()

        self.load_machines()

        # Connect UI elements to functions
        self.ui.btn_add_machine.clicked.connect(self.add_machine)
        self.ui.btn_delete_machine.clicked.connect(self.delete_machine)
        self.ui.btn_search_machine.clicked.connect(self.search_machine)

    def load_machines(self):
        self.ui.machine_list.clear()
        machines = self.model.get_machines()
        for machine in machines:
            self.ui.machine_list.addItem(
                f"{machine[0]} - {machine[3]} ({machine[2]})")  # Display ID, Name, and Serial Number

    def add_machine(self):
        name = self.ui.txt_machine_name.text()
        serial_number = self.ui.txt_serial_number.text()
        inventory_number = self.ui.txt_inventory_number.text()
        machine_type = self.ui.txt_machine_type.text()
        condition = self.ui.txt_condition.text()
        daily_rent = self.ui.txt_daily_rent.text()
        value = self.ui.txt_value.text()
        acquisition_date = self.ui.txt_acquisition_date.text()

        if not name or not serial_number or not inventory_number:
            QMessageBox.warning(self.ui, "Error", "Please fill all required fields!")
            return

        self.model.add_machine(inventory_number, serial_number, name, machine_type, condition, daily_rent, value,
                               acquisition_date)
        QMessageBox.information(self.ui, "Success", "Machine added successfully!")
        self.load_machines()

    def delete_machine(self):
        selected_item = self.ui.machine_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self.ui, "Error", "No machine selected!")
            return

        machine_id = selected_item.text().split(" - ")[0]  # Extract ID
        self.model.delete_machine(machine_id)
        QMessageBox.information(self.ui, "Success", "Machine deleted successfully!")
        self.load_machines()

    def search_machine(self):
        keyword = self.ui.txt_search.text()
        results = self.model.search_machine(keyword)

        self.ui.machine_list.clear()
        for machine in results:
            self.ui.machine_list.addItem(f"{machine[0]} - {machine[3]} ({machine[2]})")


def run():
    app = InventoryApp()
    controller = InventoryController(app)
    app.show()
    return app
