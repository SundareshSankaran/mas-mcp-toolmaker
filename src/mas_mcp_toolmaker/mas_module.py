
import os
import warnings


class MASModule:
    """This class lists out all Micro Analytic Service (MAS) modules that are available in a SAS Viya environment."""
    def __init__(self, 
                 name: str = f"MAS Module for Viya environment:{os.getenv('VIYA_HOST')}", 
                 description: str = f"This MAS Module is designed to work with the SAS Viya environment hosted at: {os.getenv('VIYA_HOST')}", 
                 version: str = "1.0.0",
                 module_types:list = ["Model", "Decision"]):
        import os
        from dotenv import load_dotenv
        import warnings
        
        # The following modules are from the folder "modules" located at the same level as this notebook.

        from mas_mcp_toolmaker.modules.get_viya_info import get_initial_count, get_all_modules, get_all_module_properties
        from mas_mcp_toolmaker.modules.get_module_info import get_module_urls, get_module_contracts
        
        from mas_mcp_toolmaker.modules.script_ram_server import build_ram_fastmcp_header, build_ram_fastmcp_tool_def, script_mcp_ram_server

        load_dotenv()

        token_check = self.check_token()

        if token_check == True:
            viya_host = os.getenv("VIYA_HOST")
            viya_access_token = os.getenv("VIYA_ACCESS_TOKEN")
            self.name = name if name else f"MAS Module for Viya environment: {os.getenv('VIYA_HOST')}"
            self.description = description if description else f"This MAS Module is designed to work with the SAS Viya environment hosted at: {os.getenv('VIYA_HOST')}"
            self.version = version if version else "1.0.0"
            self.module_types = module_types if module_types else ["Model", "Decision"]
            nbr_modules = get_initial_count(viya_host, viya_access_token)
            print(f"Number of MAS modules in the Viya environment: {nbr_modules}")
            print("Retrieving all MAS modules and their properties...")
            self.modules_properties = get_all_module_properties(viya_host, viya_access_token, get_all_modules(viya_host, viya_access_token, nbr_modules))
            print("Retrieving module URLs and contracts...")
            self.modules_urls = get_module_urls(self.modules_properties, viya_host)
            self.modules_contracts = get_module_contracts(self.modules_urls)
            if self.module_types == ["Model", "Decision"]:
                self.selected_modules = self.modules_contracts  # By default, all modules are selected for tool creation.
                print(f"MAS Module initialized with {len(self.modules_contracts)} modules ready for tool creation.")
            else:
                filtered_module_status = self.filter_module_type()
                print(filtered_module_status)

    def __str__(self):
        return f"MASModule(name={self.name}, description={self.description}, version={self.version})"
    
    def load_env_variables(self, viya_host: str = None, viya_access_token: str = None) -> str:
        """Load environment variables from a .env file."""
        from dotenv import load_dotenv
        load_dotenv()
        import getpass
        print("Environment variables reloaded from existing .env file if exists.")
        if viya_host:
            os.environ["VIYA_HOST"] = viya_host
            print(f"VIYA_HOST set to: {viya_host}")
        if viya_access_token:
            os.environ["VIYA_ACCESS_TOKEN"] = viya_access_token
            print(f"VIYA_ACCESS_TOKEN set")
        else:
            viya_access_token = getpass.getpass("Do you wish to enter new access token? Paste new token or press enter: ")
            if viya_access_token:
                os.environ["VIYA_ACCESS_TOKEN"] = viya_access_token
                print(f"VIYA_ACCESS_TOKEN updated with new token")
            else:               
                print("VIYA_ACCESS_TOKEN remains unchanged.")  
        return "Environment variables loaded successfully."
    
    def script_stdio_server(self, filename: str = "mcp_stdio_server.py") -> str:
        """Given a module contract, this method generates a Python script that serves the module as a FastMCP tool using standard input/output."""
        from mas_mcp_toolmaker.modules.get_module_info import tool_name_from_endpoint
        from mas_mcp_toolmaker.modules.script_stdio_server import py_type_for_module_type, build_stdio_fastmcp_header, build_fastmcp_tool_def, script_mcp_stdio_server
        response = script_mcp_stdio_server(filename, self.selected_modules)
        return response
    
    def script_ram_server(self, filename: str = "mcp_ram_server.py") -> str:
        """Given a module contract, this method generates a Python script that serves the module as a FastMCP tool using standard input/output."""
        from mas_mcp_toolmaker.modules.get_module_info import tool_name_from_endpoint
        from mas_mcp_toolmaker.modules.script_ram_server import py_type_for_module_type, build_ram_fastmcp_header, build_ram_fastmcp_tool_def, script_mcp_ram_server
        response = script_mcp_ram_server(filename, self.selected_modules)
        return response
    
    def check_token(self) -> bool:
        """Check if the access token is valid by making a test API call to the Viya environment."""
        if not os.getenv("VIYA_HOST") or not os.getenv("VIYA_ACCESS_TOKEN"):
            warnings.warn("Either the VIYA_HOST, the VIYA_ACCESS_TOKEN environment variable or both are not set. Please set them before initializing the MASModule.", UserWarning, stacklevel=2)
            load_env_response = self.load_env_variables()
            viya_host = os.getenv("VIYA_HOST")
            viya_access_token = os.getenv("VIYA_ACCESS_TOKEN")
            if not viya_host or not viya_access_token:
                raise EnvironmentError("Please set the VIYA_HOST and VIYA_ACCESS_TOKEN environment variables before initializing the MASModule.")
                return False
        else:
            return True
    
    def filter_module_type(self) -> str:
        """Filter the selected modules based on the specified module types (e.g., "Model", "Decision")."""
        if not self.modules_contracts:
            warnings.warn("No modules available to filter. Please ensure the MASModule is initialized correctly.", UserWarning, stacklevel=2)
            return "Warning: No modules available to filter."
        filtered_modules = [module for module in self.modules_contracts if module.get("module_type") in self.module_types]
        if not filtered_modules:
            warnings.warn(f"No modules found matching the specified types: {self.module_types}. Please check the module types and try again.", UserWarning, stacklevel=2)
            return f"Warning: No modules found matching the specified types: {self.module_types}."
        self.selected_modules = filtered_modules
        return f"Modules filtered by type. {len(self.selected_modules)} modules selected for tool creation."
    
    def list_modules(self) -> list:
        """List the names and types of the selected modules."""
        if not self.selected_modules:
            warnings.warn("No modules selected. Please ensure the MASModule is initialized correctly and modules are selected for listing.", UserWarning, stacklevel=2)
            return []
        module_list = [{"module_type": module.get("module_type"),"module_endpoint": module.get("module_endpoint"), "module_description": module.get("module_description") } for module in self.selected_modules]
        return module_list
    
    def filter_modules(self, filter_criteria: dict, condition: str = "or") -> str:
        """Filter the selected modules based on custom criteria provided as a dictionary."""
        print(f"Condition for filtering: {condition}")
        if not self.selected_modules:
            warnings.warn("No modules selected. Please ensure the MASModule is initialized correctly and modules are selected for filtering.", UserWarning, stacklevel=2)
            return "Warning: No modules selected for filtering."
        filtered_modules = self.selected_modules
        new_filtered_modules = []
        for key, value in filter_criteria.items():
            if isinstance(value, list):
                value = [v.lower() if isinstance(v, str) else v for v in value]  # Normalize string values in the list to lowercase
                for value_item in value:
                    new_filtered_module = [module for module in filtered_modules if module.get(key).lower() == value_item or (isinstance(module.get(key), list) and value_item in module.get(key).lower()) or (isinstance(module.get(key), str) and value_item in module.get(key).lower())]
                    new_filtered_modules.extend(new_filtered_module)
            else:
                value = value.lower() if isinstance(value, str) else value  # Normalize string values to lowercase
                new_filtered_module = [module for module in filtered_modules if module.get(key).lower() == value or (isinstance(module.get(key), list) and value in module.get(key).lower()) or (isinstance(module.get(key), str) and value in module.get(key).lower())]
                new_filtered_modules.extend(new_filtered_module)
        if not new_filtered_modules:
            warnings.warn(f"No modules found matching the specified filter criteria: {filter_criteria}. Please check the criteria and try again.", UserWarning, stacklevel=2)
            return f"Warning: No modules found matching the specified filter criteria: {filter_criteria}."
        self.selected_modules = new_filtered_modules
        return f"Modules filtered by criteria. {len(self.selected_modules)} modules selected for tool creation."