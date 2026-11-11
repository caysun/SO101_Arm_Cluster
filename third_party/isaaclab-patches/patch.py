from pathlib import Path

base = Path(__file__).parent

# Patch extension dependency
kit = base / "isaaclab.python.kit"
s = kit.read_text()

old = '"isaacsim.asset.importer.urdf" = {version = "2.4.31", exact = true}'
new = '"isaacsim.asset.importer.urdf" = {version = "2.4.30", exact = true}'

if old in s:
    s = s.replace(old, new)
elif new not in s:
    raise RuntimeError("Could not find URDF dependency")
kit.write_text(s)

# Patch extension version and importer method
py = base / "urdf_converter.py"
s = py.read_text()

s = s.replace(
    "isaacsim.asset.importer.urdf-2.4.31",
    "isaacsim.asset.importer.urdf-2.4.30"
)

old = "        import_config.set_merge_fixed_ignore_inertia(self.cfg.merge_fixed_joints)"
new = (
    "        if hasattr(import_config, 'set_merge_fixed_ignore_inertia'):\n"
    "            import_config.set_merge_fixed_ignore_inertia(self.cfg.merge_fixed_joints)"
)

if old in s:
    s = s.replace(old, new)
elif new not in s:
    raise RuntimeError("Could not find importer method")

py.write_text(s)

print("Both compatibility patches applied successfully.")
