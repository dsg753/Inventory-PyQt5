from PyQt5 import QtWidgets, uic
import sys


class InventoryApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("inventory.ui", self)  # Load UI from a .ui file (created using Qt Designer)

        # Connect buttons to functions
        self.btn_add_machine.clicked.connect(self.toggle_add_machine_fields)
        self.btn_delete_machine.clicked.connect(self.toggle_delete_machine_fields)
        self.btn_search_machine.clicked.connect(self.toggle_search_machine_fields)

        # Initially hide input fields
        self.add_machine_fields.setVisible(False)
        self.delete_machine_fields.setVisible(False)
        self.search_machine_fields.setVisible(False)

    def toggle_add_machine_fields(self):
        """Toggle visibility of add machine input fields."""
        if self.add_machine_fields.isVisible():
            self.add_machine_fields.setVisible(False)
        else:
            self.add_machine_fields.setVisible(True)

    def toggle_delete_machine_fields(self):
        """Toggle visibility of delete machine input fields."""
        if self.delete_machine_fields.isVisible():
            self.delete_machine_fields.setVisible(False)
        else:
            self.delete_machine_fields.setVisible(True)

    def toggle_search_machine_fields(self):
        """Toggle visibility of search machine input fields."""
        if self.search_machine_fields.isVisible():
            self.search_machine_fields.setVisible(False)
        else:
            self.search_machine_fields.setVisible(True)

    def add_machine(self):
        print("Add Machine button clicked!")

    def delete_machine(self):
        print("Delete Machine button clicked!")

    def search_machine(self):
        print("Search Machine button clicked!")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
