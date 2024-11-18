import medic.conf.parameters as cfg
import medic.ui.tabs.utils

def test_update_marks():
    # Test case where the custom value is before the default marks
    locations = list(cfg.default_marks.keys())
    values = list(cfg.default_marks.values())
    first_value = int(values[0])
    first_location = int(locations[0])
    last_value = int(values[-1])
    last_location = int(locations[-1])

    # Test case where the custom value is before the default marks
    value = first_value - 1
    marks, location = medic.ui.tabs.utils.update_marks(custom_value=value, add_all_value=False)
    assert location == first_location - cfg.custom_mark_offset
    assert isinstance(marks[str(location)], dict)

    # Test case where the custom value is after the default marks
    value = last_value + 1
    marks, location = medic.ui.tabs.utils.update_marks(custom_value=value, add_all_value=False)
    assert location == last_location + cfg.custom_mark_offset
    assert isinstance(marks[str(location)], dict)

    # Test case before and close to the last mark
    value = last_value - 1
    marks, location = medic.ui.tabs.utils.update_marks(custom_value=value, add_all_value=False)
    assert location == last_location - cfg.custom_mark_offset
    assert isinstance(marks[str(location)], dict)

    # Test case when calling add_all_value
    value = first_value - 1
    marks, location = medic.ui.tabs.utils.update_marks(custom_value=value, add_all_value=True)
    values = list(marks.values())
    assert "All" in values

    # Test case when value is exactly one of the default marks
    value = first_value
    marks, location = medic.ui.tabs.utils.update_marks(custom_value=value, add_all_value=True)
    assert str(first_location) == location
    assert "used" in marks[str(first_location)]


def test_get_index_from_marks():
    value = 1
    marks, location = medic.ui.tabs.utils.update_marks(custom_value=value, add_all_value=False)
    locations = list(marks.keys())

    # For the used case, should return -1 when add_all_value=False
    location = int(locations[0]) - cfg.custom_mark_offset
    index = medic.ui.tabs.utils.get_index_from_marks(location, marks)
    assert index == -1

    # When the first value, it should be index 0
    location = int(locations[0])
    index = medic.ui.tabs.utils.get_index_from_marks(location, marks)
    assert index == 0

    # Let's now do the add_all_values=True
    value = 1
    marks, location = medic.ui.tabs.utils.update_marks(custom_value=value, add_all_value=True)
    locations = list(marks.keys())

    # For the used case, should return -2
    location = int(locations[0]) - cfg.custom_mark_offset
    index = medic.ui.tabs.utils.get_index_from_marks(location, marks)
    assert index == -2

    # The "All" case should return -1
    location = int(list(cfg.all_mark.keys())[0])
    index = medic.ui.tabs.utils.get_index_from_marks(location, marks)
    assert index == -1

    # The first value should return 0
    location = int(locations[0])
    index = medic.ui.tabs.utils.get_index_from_marks(location, marks)
    assert index == 0