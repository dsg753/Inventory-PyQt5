import sqlite3

DB_NAME = "inventory.db"  # Define it here as well to avoid import issues


class InventoryModel:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()

    def get_machines(self):
        self.cursor.execute("SELECT * FROM machinery")
        return self.cursor.fetchall()

    def add_machine(self, inventory_number, serial_number, name, machine_type, condition, daily_rent, value,
                    acquisition_date):
        self.cursor.execute("""
            INSERT INTO machinery (inventory_number, serial_number, name, type, condition, daily_rent, value, acquisition_date, is_rented)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (inventory_number, serial_number, name, machine_type, condition, daily_rent, value, acquisition_date))
        self.conn.commit()

    def delete_machine(self, machine_id):
        self.cursor.execute("DELETE FROM machinery WHERE id = ?", (machine_id,))
        self.conn.commit()

    def search_machine(self, keyword):
        self.cursor.execute("""
            SELECT * FROM machinery WHERE name LIKE ? OR serial_number LIKE ? OR inventory_number LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
