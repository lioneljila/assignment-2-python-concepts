"""Assignment 2: demonstrations for six Python programming concepts."""

import os
import random
import socket
import sqlite3
import threading
from abc import ABC, abstractmethod


def run_question_one():
    """SQLite connection, table creation, insertion, retrieval, and cleanup."""
    database = "scholars_repository.db"
    connection = sqlite3.connect(database)
    try:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS apprentices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apprentice_name TEXT NOT NULL,
            scholastic_rank INTEGER NOT NULL,
            sanctuary_city TEXT NOT NULL
        )""")
        cursor.execute("DELETE FROM apprentices")
        records = [
            ("Bartholomew Sterling", 5, "Edinburgh"),
            ("Gwendolyn Vance", 4, "Canterbury"),
            ("Algernon Blackwood", 6, "Oxford"),
            ("Clementine Frost", 5, "Cambridge"),
        ]
        cursor.executemany(
            "INSERT INTO apprentices (apprentice_name, scholastic_rank, sanctuary_city) VALUES (?, ?, ?)",
            records,
        )
        connection.commit()
        print("Question 1:", cursor.execute("SELECT * FROM apprentices").fetchall())
    finally:
        connection.close()
        if os.path.exists(database):
            os.remove(database)


class BankAccount:
    """Bank account demonstrating encapsulation with a private balance."""

    def __init__(self, vault_custodian, initial_treasure=0.0):
        self.vault_custodian = vault_custodian
        self.__quicksilver_balance = max(0.0, float(initial_treasure))

    def deposit(self, incoming_tribute):
        if incoming_tribute > 0:
            self.__quicksilver_balance += incoming_tribute
            print(f"[{self.vault_custodian}] Deposited: ${incoming_tribute:.2f}")
        else:
            print("Deposit failed: amount must be greater than 0.")

    def withdraw(self, outgoing_tribute):
        if outgoing_tribute <= 0:
            print("Withdrawal failed: amount must be greater than 0.")
        elif outgoing_tribute > self.__quicksilver_balance:
            print("Withdrawal denied: insufficient reserves.")
        else:
            self.__quicksilver_balance -= outgoing_tribute
            print(f"[{self.vault_custodian}] Withdrew: ${outgoing_tribute:.2f}")

    def display_balance(self):
        print(f"[{self.vault_custodian}] Balance: ${self.__quicksilver_balance:.2f}")
        return self.__quicksilver_balance


def run_question_two():
    print("Question 2:")
    account = BankAccount("Wilhelmina", 250)
    account.display_balance()
    account.deposit(150)
    account.withdraw(80)
    account.withdraw(500)
    account.display_balance()
    try:
        print(account.__quicksilver_balance)
    except AttributeError as error:
        print("Encapsulation blocked direct access:", error)


def sentinel_server_worker(host, port, ready):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((host, port))
            server.listen(1)
            server.settimeout(5)
            ready.set()
            connection, address = server.accept()
            with connection:
                message = connection.recv(1024).decode("utf-8")
                print(f"Server received from {address}: {message}")
    except socket.error as error:
        print("Server network error:", error)


def emissary_client_worker(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(5)
            client.connect((host, port))
            message = "Hello from client!"
            client.sendall(message.encode("utf-8"))
            print("Client sent:", message)
    except socket.error as error:
        print("Client network error:", error)


def run_question_three():
    print("Question 3:")
    host, port = "127.0.0.1", 55432
    ready = threading.Event()
    server = threading.Thread(target=sentinel_server_worker, args=(host, port, ready))
    server.start()
    ready.wait(2)
    emissary_client_worker(host, port)
    server.join(3)


def run_question_four():
    values = [random.uniform(0.0, 10.0) for _ in range(5)]
    print("Question 4:", [f"{value:.4f}" for value in values])
    print("Minimum:", min(values), "Maximum:", max(values))


class FileHandler(ABC):
    @abstractmethod
    def read(self, parchment_identifier):
        pass

    @abstractmethod
    def write(self, parchment_identifier, manuscript_payload):
        pass


class TextFileHandler(FileHandler):
    def read(self, parchment_identifier):
        try:
            with open(parchment_identifier, encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return None

    def write(self, parchment_identifier, manuscript_payload):
        with open(parchment_identifier, "w", encoding="utf-8") as file:
            file.write(str(manuscript_payload))


class BinaryFileHandler(FileHandler):
    def read(self, parchment_identifier):
        try:
            with open(parchment_identifier, "rb") as file:
                return file.read()
        except FileNotFoundError:
            return None

    def write(self, parchment_identifier, manuscript_payload):
        data = manuscript_payload.encode("utf-8") if isinstance(manuscript_payload, str) else manuscript_payload
        with open(parchment_identifier, "wb") as file:
            file.write(data)


def run_question_five():
    print("Question 5:")
    text_path, binary_path = "whimsical_prose.txt", "quicksilver_bytes.bin"
    try:
        text = TextFileHandler()
        binary = BinaryFileHandler()
        text.write(text_path, "Exploring Python with uncommon curiosity and elegance!")
        print(text.read(text_path))
        binary.write(binary_path, b"Raw binary payload: \x00\x01\x02\xff")
        print(binary.read(binary_path))
        try:
            FileHandler()
        except TypeError as error:
            print("Abstract class blocked instantiation:", error)
    finally:
        for path in (text_path, binary_path):
            if os.path.exists(path):
                os.remove(path)


class Vehicle:
    def __init__(self, conveyance_archetype, navigator_name):
        self.conveyance_archetype = conveyance_archetype
        self.navigator_name = navigator_name

    def move(self):
        print(f"{self.navigator_name}'s {self.conveyance_archetype} moves forward.")


class Car(Vehicle):
    def __init__(self, conveyance_archetype, navigator_name, wheel_assemblies=4):
        super().__init__(conveyance_archetype, navigator_name)
        self.wheel_assemblies = wheel_assemblies

    def move(self):
        print(f"{self.navigator_name}'s car revs its engine on {self.wheel_assemblies} wheels.")


class Bike(Vehicle):
    def __init__(self, conveyance_archetype, navigator_name, has_tinkling_chime=True):
        super().__init__(conveyance_archetype, navigator_name)
        self.has_tinkling_chime = has_tinkling_chime

    def move(self):
        sound = "ringing its chime" if self.has_tinkling_chime else "gliding quietly"
        print(f"{self.navigator_name}'s bicycle pedals rhythmically, {sound}.")


def run_question_six():
    print("Question 6:")
    for vehicle in (Vehicle("Vintage Locomotive", "Peregrine"), Car("Aston Martin DB5", "Montgomery"), Bike("Penny-Farthing", "Gwendolyn")):
        vehicle.move()


if __name__ == "__main__":
    run_question_one()
    run_question_two()
    run_question_three()
    run_question_four()
    run_question_five()
    run_question_six()
