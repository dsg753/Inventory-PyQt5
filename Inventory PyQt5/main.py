from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
import os



# Import the database setup and models
from database import engine, Base, МашиниИнвентар, МашиниПодНаем

# Create database session
Session = sessionmaker(bind=engine)
session = Session()

class InventoryApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Get the directory of the current script
        base_dir = os.path.dirname(__file__)
        # Construct the path to the .ui file
        ui_path = os.path.join(base_dir, "inventory.ui")
        uic.loadUi(ui_path, self)

        # Pagination variables
        self.inventory_page = 0
        self.inventory_page_size = 100  # Number of items per page
        self.rental_page = 0
        self.rental_page_size = 100  # Number of items per page

        # Connect inventory tab buttons
        self.btn_add_inventory.clicked.connect(self.show_inventory_inputs)
        self.btn_save_inventory.clicked.connect(self.add_inventory_item)
        self.btn_delete_inventory.clicked.connect(self.delete_inventory_item)
        self.inventory_search_input.textChanged.connect(self.filter_inventory_data)
        self.btn_next_inventory_page.clicked.connect(self.next_inventory_page)
        self.btn_prev_inventory_page.clicked.connect(self.prev_inventory_page)

        # Connect rental tab buttons
        self.btn_add_rental.clicked.connect(self.show_rental_inputs)
        self.btn_save_rental.clicked.connect(self.add_rental_item)
        self.btn_delete_rental.clicked.connect(self.delete_rental_item)
        self.rental_search_input.textChanged.connect(self.filter_rental_data)
        self.btn_next_rental_page.clicked.connect(self.next_rental_page)
        self.btn_prev_rental_page.clicked.connect(self.prev_rental_page)

        # Initialize data
        self.load_inventory_data()
        self.load_rental_data()

        # Initially hide input forms
        self.inventory_inputs_frame.hide()
        self.rental_inputs_frame.hide()

    def show_inventory_inputs(self):
        """Toggle inventory input form visibility."""
        self.inventory_inputs_frame.setVisible(
            not self.inventory_inputs_frame.isVisible()
        )

    def show_rental_inputs(self):
        """Toggle rental input form visibility."""
        self.rental_inputs_frame.setVisible(
            not self.rental_inputs_frame.isVisible()
        )

    def add_inventory_item(self):
        """Add new inventory item."""
        try:
            new_item = МашиниИнвентар(
                инвентарен_номер=self.inventory_number_input.text().strip(),
                сериен_номер=self.serial_number_input.text().strip(),
                име=self.name_input.text().strip(),
                тип=self.type_input.text().strip(),
                състояние=self.condition_input.text().strip(),
                стойност=float(self.value_input.text().strip()),
                дата_на_придобиване=self.date_input.date().toPyDate()
            )
            
            if not all([new_item.инвентарен_номер, new_item.сериен_номер, 
                       new_item.име, new_item.тип, new_item.състояние, new_item.стойност]):
                raise ValueError("Всички полета са задължителни!")

            session.add(new_item)
            session.commit()
            self.load_inventory_data()
            self.clear_inventory_inputs()
            self.inventory_inputs_frame.hide()
            QMessageBox.information(self, "Успешно", "Машината беше добавена успешно!")
            
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Грешка", str(e))

    def add_rental_item(self):
        """Add new rental item."""
        try:
            инвентарен_номер = self.rental_inventory_number_input.text().strip()
            сериен_номер = self.rental_serial_number_input.text().strip()

            # Check if the machine exists in the inventory
            existing_item = session.query(МашиниИнвентар).filter_by(
                инвентарен_номер=инвентарен_номер, сериен_номер=сериен_номер
            ).first()

            if not existing_item:
                raise ValueError("Машина с този сериен номер или инвентарен номер не съществува!")

            new_item = МашиниПодНаем(
                инвентарен_номер=инвентарен_номер,
                сериен_номер=сериен_номер,
                име=self.rental_name_input.text().strip(),
                дневен_наем=float(self.daily_rate_input.text().strip()),
                стойност=float(self.rental_value_input.text().strip()),
                дата_на_последна_поддръжка=self.maintenance_date_input.date().toPyDate()
            )

            if not all([new_item.инвентарен_номер, new_item.сериен_номер, 
                       new_item.име, new_item.дневен_наем, new_item.стойност]):
                raise ValueError("Всички полета са задължителни!")

            session.add(new_item)
            session.commit()
            self.load_rental_data()
            self.clear_rental_inputs()
            self.rental_inputs_frame.hide()
            QMessageBox.information(self, "Успешно", "Машината беше добавена успешно!")

        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Грешка", str(e))

    def delete_inventory_item(self):
        """Delete selected inventory item."""
        current_row = self.inventory_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Моля, изберете ред за изтриване!")
            return

        reply = QMessageBox.question(self, "Потвърждение", 
                                   "Сигурни ли сте, че искате да изтриете този запис?",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                item_id = int(self.inventory_table.item(current_row, 0).text())
                item = session.query(МашиниИнвентар).get(item_id)
                if item:
                    session.delete(item)
                    session.commit()
                    self.load_inventory_data()
                    QMessageBox.information(self, "Успешно", "Записът беше изтрит успешно!")
            except Exception as e:
                session.rollback()
                QMessageBox.critical(self, "Грешка", str(e))

    def delete_rental_item(self):
        """Delete selected rental item."""
        current_row = self.rental_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Моля, изберете ред за изтриване!")
            return

        reply = QMessageBox.question(self, "Потвърждение", 
                                   "Сигурни ли сте, че искате да изтриете този запис?",
                                   QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                item_id = int(self.rental_table.item(current_row, 0).text())
                item = session.query(МашиниПодНаем).get(item_id)
                if item:
                    session.delete(item)
                    session.commit()
                    self.load_rental_data()
                    QMessageBox.information(self, "Успешно", "Записът беше изтрит успешно!")
            except Exception as e:
                session.rollback()
                QMessageBox.critical(self, "Грешка", str(e))

    def filter_inventory_data(self):
        """Filter inventory table based on search input."""
        search_text = self.inventory_search_input.text().lower()
        for row in range(self.inventory_table.rowCount()):
            match = False
            for col in range(1, 5):  # Search in inventory number, serial number, name, and rental status
                item = self.inventory_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.inventory_table.setRowHidden(row, not match)

    def filter_rental_data(self):
        """Filter rental table based on search input."""
        search_text = self.rental_search_input.text().lower()
        for row in range(self.rental_table.rowCount()):
            match = False
            for col in range(1, 4):  # Search in inventory number, serial number, and name
                item = self.rental_table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.rental_table.setRowHidden(row, not match)

    def load_inventory_data(self):
        """Load inventory data into table with pagination."""
        self.inventory_table.setRowCount(0)
        items = session.query(МашиниИнвентар).offset(self.inventory_page * self.inventory_page_size).limit(self.inventory_page_size).all()
        for row, item in enumerate(items):
            self.inventory_table.insertRow(row)
            self.inventory_table.setItem(row, 0, QTableWidgetItem(str(item.id)))
            self.inventory_table.setItem(row, 1, QTableWidgetItem(item.инвентарен_номер))
            self.inventory_table.setItem(row, 2, QTableWidgetItem(item.сериен_номер))
            self.inventory_table.setItem(row, 3, QTableWidgetItem(item.име))
            self.inventory_table.setItem(row, 4, QTableWidgetItem(item.тип))
            self.inventory_table.setItem(row, 5, QTableWidgetItem(str(item.стойност)))
            self.inventory_table.setItem(row, 6, QTableWidgetItem(item.състояние))
            if item.дата_на_придобиване:
                date_str = item.дата_на_придобиване.strftime('%Y-%m-%d')
            else:
                date_str = ""
            self.inventory_table.setItem(row, 7, QTableWidgetItem(date_str))
            
            # Check if the machine is rented
            rented_item = session.query(МашиниПодНаем).filter_by(инвентарен_номер=item.инвентарен_номер, сериен_номер=item.сериен_номер).first()
            if rented_item:
                self.inventory_table.setItem(row, 8, QTableWidgetItem("Да"))
            else:
                self.inventory_table.setItem(row, 8, QTableWidgetItem("Не"))

    def load_rental_data(self):
        """Load rental data into table with pagination."""
        self.rental_table.setRowCount(0)
        items = session.query(МашиниПодНаем).offset(self.rental_page * self.rental_page_size).limit(self.rental_page_size).all()
        for row, item in enumerate(items):
            self.rental_table.insertRow(row)
            self.rental_table.setItem(row, 0, QTableWidgetItem(str(item.id)))
            self.rental_table.setItem(row, 1, QTableWidgetItem(item.инвентарен_номер))
            self.rental_table.setItem(row, 2, QTableWidgetItem(item.сериен_номер))
            self.rental_table.setItem(row, 3, QTableWidgetItem(item.име))
            self.rental_table.setItem(row, 4, QTableWidgetItem(str(item.дневен_наем)))
            self.rental_table.setItem(row, 5, QTableWidgetItem(str(item.стойност)))
            if item.дата_на_последна_поддръжка:
                date_str = item.дата_на_последна_поддръжка.strftime('%Y-%m-%d')
            else:
                date_str = ""
            self.rental_table.setItem(row, 6, QTableWidgetItem(date_str))

    def next_inventory_page(self):
        """Go to the next page of inventory data."""
        self.inventory_page += 1
        self.load_inventory_data()

    def prev_inventory_page(self):
        """Go to the previous page of inventory data."""
        if self.inventory_page > 0:
            self.inventory_page -= 1
            self.load_inventory_data()

    def next_rental_page(self):
        """Go to the next page of rental data."""
        self.rental_page += 1
        self.load_rental_data()

    def prev_rental_page(self):
        """Go to the previous page of rental data."""
        if self.rental_page > 0:
            self.rental_page -= 1
            self.load_rental_data()

    def clear_inventory_inputs(self):
        """Clear all inventory input fields."""
        self.inventory_number_input.clear()
        self.serial_number_input.clear()
        self.name_input.clear()
        self.type_input.clear()
        self.value_input.clear()
        self.condition_input.clear()
        self.date_input.setDate(QDate.currentDate())

    def clear_rental_inputs(self):
        """Clear all rental input fields."""
        self.rental_inventory_number_input.clear()
        self.rental_serial_number_input.clear()
        self.rental_name_input.clear()
        self.daily_rate_input.clear()
        self.rental_value_input.clear()
        self.maintenance_date_input.setDate(QDate.currentDate())

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
