from data_storage import DataStorageSystem
from commands import CommandProcessor


def main():
    data_storage_system = DataStorageSystem()
    command_processor = CommandProcessor(data_storage_system)

    data_storage = DataStorageSystem()
    data_storage_system.add_pool("pool1")
    data_storage_system.print_pools()

    data_storage_system.remove_pool("pool1")
    data_storage_system.print_pools()

    data_storage_system.add_pool("pool1")
    data_storage_system.get_pool("pool1")
    data_storage_system.get_pool("pool1")
    data_storage_system.print_pools()

    data_storage_system.add_pool("pool2")
    data_storage_system.print_pools()

    print("Entering interactive mode. Enter commands or type 'exit' to quit.")

    while True:
        command = input("> ")

        if command.lower() == 'exit':
            break

        command_processor.process_command(command)

    print("Exiting interactive mode.")


if __name__ == "__main__":

    main()
