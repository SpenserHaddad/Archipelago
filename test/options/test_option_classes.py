import unittest
from typing import Any

from Options import Choice, DefaultOnToggle, Option, OptionDict, OptionError, OptionList, OptionSet, Toggle


class TestNumericOptions(unittest.TestCase):
    def test_numeric_option(self) -> None:
        """Tests the initialization and equivalency comparisons of the base Numeric Option class."""
        class TestChoice(Choice):
            option_zero = 0
            option_one = 1
            option_two = 2
            alias_three = 1
            non_option_attr = 2

        class TestToggle(Toggle):
            pass

        class TestDefaultOnToggle(DefaultOnToggle):
            pass

        with self.subTest("choice"):
            choice_option_default = TestChoice.from_any(TestChoice.default)
            choice_option_string = TestChoice.from_any("one")
            choice_option_int = TestChoice.from_any(2)
            choice_option_alias = TestChoice.from_any("three")
            choice_option_attr = TestChoice.from_any(TestChoice.option_two)
            
            self.assertEqual(choice_option_default, TestChoice.option_zero,
                "assigning default didn't match default value")
            self.assertEqual(choice_option_string, "one")
            self.assertEqual(choice_option_int, 2)
            self.assertEqual(choice_option_alias, TestChoice.alias_three)
            self.assertEqual(choice_option_attr, TestChoice.non_option_attr)

            self.assertRaises(KeyError, TestChoice.from_any, "four")
            
            self.assertIn(choice_option_int, [1, 2, 3])
            self.assertIn(choice_option_int, {2})
            self.assertIn(choice_option_int, (2,))

            self.assertIn(choice_option_string, ["one", "two", "three"])
            # this fails since the hash is derived from the value
            self.assertNotIn(choice_option_string, {"one"})
            self.assertIn(choice_option_string, ("one",))

        with self.subTest("toggle"):
            toggle_default = TestToggle.from_any(TestToggle.default)
            toggle_string = TestToggle.from_any("false")
            toggle_int = TestToggle.from_any(0)
            toggle_alias = TestToggle.from_any("off")

            self.assertFalse(toggle_default)
            self.assertFalse(toggle_string)
            self.assertFalse(toggle_int)
            self.assertFalse(toggle_alias)

        with self.subTest("on toggle"):
            toggle_default = TestDefaultOnToggle.from_any(TestDefaultOnToggle.default)
            toggle_string = TestDefaultOnToggle.from_any("true")
            toggle_int = TestDefaultOnToggle.from_any(1)
            toggle_alias = TestDefaultOnToggle.from_any("on")

            self.assertTrue(toggle_default)
            self.assertTrue(toggle_string)
            self.assertTrue(toggle_int)
            self.assertTrue(toggle_alias)


class TestVerifyKeys(unittest.TestCase):
    def test_invalid_key_raises_option_error(self) -> None:
        class TestOptionDict(OptionDict):
            default = {"A": 1}
            display_name = "Test Option Dict"
            valid_keys = ("A", "r", "c", "h", "i")

        class TestOptionList(OptionList):
            default = ("A", "A", "r", "r")
            display_name = "Test Option List"
            valid_keys = ("A", "r", "c", "h", "i")

        class TestOptionSet(OptionSet):
            default = frozenset("A")
            display_name = "Test Option Set"
            valid_keys = ("A", "r", "c", "h", "i")

        sub_test_info: list[tuple[type[Option], Any, str | None]] = [
            (TestOptionDict, {"A": 1, "r": 10, "B": 4, "K": 5}, None),
            (TestOptionList, ["A", "A", "B", "K", "r", "i"], "A,A,r,B,i,K,c,h,i"),
            (TestOptionSet, ("A", "r", "c", "B", "K"), "A,r,c,h,B,K"),
        ]

        for verify_keys_cls, from_any_arg, from_text_arg in sub_test_info:
            with self.subTest(cls=verify_keys_cls.__name__):
                # "B" or "K" should trigger the exception.
                self.assertRaises(OptionError, verify_keys_cls.from_any, from_any_arg)
                # OptionDict has no from_text option, so check if the method exists on the class first
                if (from_text := getattr(verify_keys_cls, "from_text", None)) is not None:
                    self.assertRaises(OptionError, from_text, from_text_arg)
