# Micro Analytic Service (MAS) - Model Context Protocol (MCP) Tool Maker

This repository contains a Python package to programmatically create a Model Context Protocol (MCP) server script calling published SAS Micro Analytic Services (MAS) modules discovered in a SAS Viya environment. The output is a Python script (in two flavours) which can be used to stand up an MCP server through stdio, Streamable HTTP (planned) and a format customised for SAS Retrieval Agent Manager (RAM).

<mark> Python package at: https://pypi.org/project/mas-mcp-toolmaker/ </mark>

A wiki of this repo has been generated using DeepWiki and is available here: [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/SundareshSankaran/mas-mcp-toolmaker)

Note that this open-source package is provided as a convenient way to interface with a SAS Viya environment in an MCP context.  SAS Viya is proprietary software from [SAS Institute](https://www.sas.com/) through several offerings. Running operations in SAS Viya requires a license and functioning credentials.


## Installation & Set up
1. Requirements: Python 3.12 or later
2. Access to a SAS Viya environment with SAS Micro Analytic Service (MAS).  This is typically a SAS Viya Enterprise or SAS Viya Advanced offering. Refer this [page](https://www.sas.com/en_us/software/viya.html) for details.
3. While not mandatory, it's recommended to stand up a virtual environment before installing this package.  A convenient shell script [`build.sh`](./build/build.sh) is provided for this purpose.  Refer this [repository](https://github.com/SundareshSankaran/build-script) for a starter build script.  
4. The simplest way is to pip install this package from pypi.org
```
pip install mas-mcp-toolmaker
```
5. In case you would like to perform a local install,
```
pip install -e .
```
6. Use a .env file (refer [`sample.env`](https://github.com/SundareshSankaran/mas-mcp-toolmaker/blob/main/sample.env), create a copy and rename to `.env`) to set environment variables for the following:
   (Refer this link for more details on obtaining access tokens: [Authentication to SAS Viya: a couple of approaches](https://blogs.sas.com/content/sgf/2023/02/07/authentication-to-sas-viya/))
   - VIYA_HOST: A URL pointing to your SAS Viya environment
   - VIYA_ACCESS_TOKEN: An access token which helps you authenticate to SAS Viya

## Quick Start: Running the notebook

```bash
# if using virtual environment (use Windows equivalent where applicable)
cd build
. buildproj/bin/activate
jupyter-lab
```

The notebook [`mas-mcp-toolmaker.ipynb`](https://github.com/SundareshSankaran/mas-mcp-toolmaker/blob/main/mas-mcp-toolmaker.ipynb) contains further details.

## Quick Start: Basic Commands

Using this package is very simple.  At a fundamental level, there are two basic operations involved. 

1. Generating a list of MAS modules from a SAS Viya environment

```python
from mas_mcp_toolmaker import MASModule

masm = MASModule()

```

2. Writing the extracted modules in tool representation to an MCP server script of your chosen flavour.

```python
masm.script_stdio_server("your_server_file.py")

# or 

masm.script_ram_server("your_ram_server_file.py")
```

Refer the notebook for other functions.


## Contact
   - Sundaresh Sankaran ([email](sundaresh.sankaran@gmail.com))

## Version
   - Version 1.1.0 (31MAY2026)
   - Version 1.0 (13MAY2026)
