import os
import xml.etree.ElementTree as ET
import shutil

def delete_reference_item_group (xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Remove existing ItemGroup elements
    existing_item_groups = root.findall('.//ItemGroup')
    for item_group in existing_item_groups:
        references = item_group.findall('.//Reference')
        if len(references) > 0:
            root.remove(item_group)
        elif len(item_group) == 0:
            root.remove(item_group)

    # Write the changes back to the XML file
    tree.write(xml_file)

def add_reference_items(xml_file, dlls, source_path):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Create a new ItemGroup element and add references to it
    new_item_group = ET.Element("ItemGroup")
    new_item_group.text = "\n\t\t"
    for dll in dlls:
        ref_elem = ET.Element("Reference")
        ref_elem.set("Include", os.path.splitext(dll)[0])
        ref_elem.text = "\n\t\t\t"

        if dll != dlls[len(dlls)-1]:
            ref_elem.tail = "\n\t\t"
        else:
            ref_elem.tail =  "\n\t"

        hint_path_elem = ET.Element("HintPath")
        hint_path_elem.text = source_path + "\\" + dll

        hint_path_elem.tail = "\n\t\t"

        ref_elem.append(hint_path_elem)
        new_item_group.append(ref_elem)
        
        new_item_group.tail = "\n"

    # Append the new ItemGroup to the root
    root.append(new_item_group)

    # Write the changes back to the XML file
    tree.write(xml_file)

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

def copy_files(source_directory, destination_directory, files_to_copy):
    try:
        # Check if the destination directory exists, if not, create it
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        # Iterate over the list of files to copy
        for file_name in files_to_copy:
            source_file_path = os.path.join(source_directory, file_name)
            destination_file_path = os.path.join(destination_directory, file_name)
            
            # Check if the source file exists
            if os.path.exists(source_file_path):
                # Copy the file
                shutil.copy2(source_file_path, destination_file_path)
                print(f"File {file_name} copied successfully ")
                print(f"from {source_file_path} to {destination_file_path}")
                print(f"")
            else:
                print(f"File {file_name} does not exist.")
                print(f"Source Path: {source_file_path}")
                print(f"")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    setupSettingsPath="..\\SetupSettings.cfg"
    projectPath=".."

    gameDirectory= read_configuration("gameDirectory", "[Game]")

    source_directory = gameDirectory + "\\Astrea_Data\\Managed"
    destination_directory = projectPath + "\\libs"

    dlls = []
    dlls = read_configuration('', '[DLLs]')

    # Copy
    copy_files(source_directory, destination_directory, dlls)

    for filename in os.listdir(projectPath):
        if filename.endswith('.csproj'):
            delete_reference_item_group(projectPath+"\\"+filename)
            add_reference_items(projectPath+"\\"+filename, dlls, "libs")
    
    print(f"Finished to add References on .csproj")
