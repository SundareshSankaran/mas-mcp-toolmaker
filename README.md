# Microanalytics Services (MAS) - Model Context Protocol (MCP) Tool Maker

This notebook helps you programmatically create a Model Context Protocol (MCP) server script calling published SAS Micro Analytic Service (MAS) modules discovered in a SAS Viya environment. The output is a Python script (in two flavours) which can be used to stand up an MCP server through stdio, Streamable HTTP (planned) and SAS Retrieval Agent Manager.

A wiki of this repo has been generated using DeepWiki and is available here: [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/SundareshSankaran/mas-mcp-toolmaker)

## Installation & Set up
1. Requirements: Python 3.12 or later and access to a SAS Viya Advanced / SAS Viya Enterprise offering
2. Ensure your Python environment has the following packages from [`requirements.txt`](./build/requirements.txt) installed.
3. Alternatively, you can build a virtual environment for this project through the following script located in the[`build`](./build) folder: [`build.sh`](./build/build.sh)
4. Use a .env file (refer [`sample.env`](./sample.env), create a copy and rename to `.env`) to set environment variables for the following:
   (Refer this link for more details on obtaining access tokens: [Authentication to SAS Viya: a couple of approaches](https://blogs.sas.com/content/sgf/2023/02/07/authentication-to-sas-viya/))
   - VIYA_HOST: A URL pointing to your SAS Viya environment
   - VIYA_ACCESS_TOKEN: An access token which helps you authenticate to SAS Viya

## Running the notebook

```bash
# if using virtual environment (use Windows equivalent where applicable)
cd build
. buildproj/bin/activate
jupyter-lab
```

The notebook [`mas-mcp-toolmaker.ipynb`](./mas-mcp-toolmaker.ipynb) contains further details.

## Contact
   - Sundaresh Sankaran ([email](sundaresh.sankaran@gmail.com))

## Version
   - Version 1.0.1 (29MAY2026)
   - Version 1.0.0 (13MAY2026)
