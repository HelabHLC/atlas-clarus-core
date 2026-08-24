# Installation — ATLAS Clarus × Krita v0.3.4

## Before installation

This is a custom Python plugin. Review the source and checksums before installing it. A Krita Python plugin executes with the permissions of Krita and can access files available to the application.

Compatibility is established only for the recorded validation environment. The exact Krita application version and universal platform compatibility were not captured in the frozen manifest, so no broader compatibility claim is made.

## Install with Krita's plugin importer

1. Download `ATLAS_Clarus_Krita_v0_3_4_FULL_MASTER_SEARCH.zip` from this directory.
2. Verify its SHA-256:

   `a702a1125bfa4a86cb7eb8d7ba09155c33d0e49b21bf3ec55eaa45ce9625ed29`

3. In Krita, choose **Tools → Scripts → Import Python Plugin…**.
4. Select the downloaded ZIP and confirm the import.
5. Restart Krita.
6. Open **Settings → Configure Krita… → Python Plugin Manager**.
7. Enable **ATLAS Clarus PKL · Engineering Beta v0.3.4**.
8. Restart Krita again.
9. Open the docker through **Settings → Dockers → ATLAS Clarus PKL**.

These steps follow Krita's official custom Python plugin workflow:

https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html

## Manual installation fallback

Extract the plugin ZIP. Copy:

- `atlas_clarus_pkl.desktop`
- the complete `atlas_clarus_pkl/` directory

into Krita's `pykrita` resource directory. Krita exposes the resource location through **Settings → Manage Resources → Open Resource Folder**. Restart Krita, enable the plugin in the Python Plugin Manager and restart again.

## First verification

1. Confirm that the docker reports `Full PKL master: 13283 rows`.
2. Clear the search query and confirm that the full master remains available.
3. For an exact known input, compare the returned `atlas_row_id`, reference, PKL RGB/HEX and `d²_RGB` against the frozen manifest.

Do not interpret a successful installation or digital lookup as physical colour measurement or print approval.
