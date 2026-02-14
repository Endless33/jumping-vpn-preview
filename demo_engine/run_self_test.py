from self_test import SelfTest

if __name__ == "__main__":
    test = SelfTest()
    errors = test.run()
    test.print_result(errors)