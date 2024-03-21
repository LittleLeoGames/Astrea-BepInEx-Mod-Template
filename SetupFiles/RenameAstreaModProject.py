import os
import xml.etree.ElementTree as ET
import re
import fileinput

def read_configuration(attribute, section):
    with open(setupSettingsPath, 'r') as file:
        # Read lines until encountering an empty line
        lines = []
        for line in file:
            line = line.strip()
            if not line:
                break
            lines.append(line)

    section = section.replace('[','')
    section = section.replace(']','')
    section = "[" + section + "]"

    found=False
    # Process the lines to extract assembly name
    if (attribute == ''):
        attribute_value = []
    else:
        attribute_value = ""

    for line in lines:
        line = line.strip()
        if not found and line == section:
            found=True
        elif found:
            parts = line.split('=')
            if attribute != '' and len(parts) == 2 and parts[0].strip() == attribute:
                attribute_value = parts[1].strip().replace('"','')
                break
            elif attribute == '':
                if len(parts) == 2 and parts[0] == '' or parts[0].find("[") != -1:
                    break

                attribute_value.append(parts[0].replace('"',''))

    return attribute_value

def rename_project(oldName, newName):
    # Specify the current and new filenames
    current_filename = oldName
    new_filename = newName

    # Rename the file
    os.rename(current_filename, new_filename)

    print(f"File '{current_filename}' has been renamed to '{new_filename}'.")

def rename_assembly(projectPath, newAssemblyName):
    # Load the XML file
    tree = ET.parse(projectPath)
    root = tree.getroot()

    # Find the PropertyGroup element
    property_group = root.find('./PropertyGroup')

    # Find the AssemblyName and Description elements
    assembly_name = property_group.find('AssemblyName')
    description = property_group.find('Description')

    # Update their text
    assembly_name.text = newAssemblyName
    description.text = newAssemblyName + " description"

    # Save the changes to the file
    tree.write(projectPath)

# Function to replace the old namespace with a new one in a C# script
def replace_namespace(file_path, new_namespace):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Iterate through each line and perform the replacement
    modified_lines = []
    for line in lines:
        modified_line = line
        if line.find("namespace") != -1:
            parts = line.split(' ')
            if len(parts) == 2:
                parts = parts[1].split('.')
                if len(parts) > 1:
                    modified_line = "namespace " + new_namespace
                    for i in range(1, len(parts)):
                        modified_line += "." + parts[i]
                else:
                    modified_line = "namespace " + new_namespace + "\n"
            else:
                modified_line = "namespace " + new_namespace + "\n"
        
        modified_lines.append(modified_line)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(modified_lines)

    print(f"Replaced namespace with '{new_namespace}' in file '{file_path}'.")

def change_assembly_name(file_path, new_assembly_name):
    # Iterate over lines in the file
    for line in fileinput.input(file_path, inplace=True):
        # Find lines containing PLUGIN_GUID and PLUGIN_NAME
        if line.strip().startswith("public const string PLUGIN_GUID ="):
            # Find the last dot in the line
            last_dot_index = line.rfind('.')
            # Replace the value of PLUGIN_GUID, preserving the initial part
            line = line[:last_dot_index + 1] + new_assembly_name + '";\n'
        elif line.strip().startswith("public const string PLUGIN_NAME ="):
            # Find the last dot in the line
            last_dot_index = line.rfind('.')
            # Replace the value of PLUGIN_NAME, preserving the initial part
            line = line[:last_dot_index + 1] + new_assembly_name + '";\n'

        # Print the modified line to stdout
        print(line, end='')

if __name__ == "__main__":
    setupSettingsPath="..\\SetupSettings.cfg"
    projectPath = ".."
    
    assemblyName= read_configuration("assemblyName", "[Project]")
    pluginScriptPath = "..\\Plugin.cs"
    myPlugininfoScriptPath = "..\\MyPluginInfo.cs"

    replace_namespace(myPlugininfoScriptPath, assemblyName)
    replace_namespace(pluginScriptPath, assemblyName)

    for filename in os.listdir(projectPath):
        if filename.endswith('.csproj'):
            rename_project(projectPath+"\\"+filename, projectPath+"\\"+assemblyName+".csproj")
            rename_assembly(projectPath+"\\"+assemblyName+".csproj", assemblyName)
            change_assembly_name(myPlugininfoScriptPath, assemblyName)

            for root, dirs, files in os.walk(projectPath+"\\Patches"):
                for file in files:
                    if file.endswith(".cs"):
                        file_path = os.path.join(root, file)
                        replace_namespace(file_path, assemblyName)
                    

            
