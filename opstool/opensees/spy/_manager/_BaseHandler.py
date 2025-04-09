from collections import defaultdict

class BaseHandler:

    nodal_mass = defaultdict(lambda: 0.0)
    ele_load_surface = defaultdict(lambda: 0.0)
    ele_load_solid = defaultdict(lambda: 0.0)

    def handles(self) -> list[str]:
        """Return a list of function names this handler can process."""
        raise NotImplementedError

    def handle(self, func_name: str, arg_map: dict):
        """Process the function call."""
        raise NotImplementedError

    def clear(self):
        """Reset internal data"""
        raise NotImplementedError

    @staticmethod
    def _extract_args_by_str(lst: list, target_keys):
        result = []
        found = False
        if not isinstance(target_keys, str):
            target_keys = set(target_keys)
        else:
            target_keys = [target_keys]
        for item in lst:
            if found:
                if isinstance(item, str):
                    break
                result.append(item)
            elif item in target_keys:
                found = True
        return result

    @classmethod
    def _add_nodal_mass(cls, tag: int, mass: float):
        cls.nodal_mass[tag] += mass

