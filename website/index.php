<?php
// Get the 'id', 'xml', 'hosted', and 'versions' parameters from the URL
$id = isset($_GET['id']) ? urldecode($_GET['id']) : null;
$xml = isset($_GET['xml']);  // Check if 'xml' parameter exists (whether it's true or not)
$hosted = isset($_GET['hosted']); // Check if 'hosted' parameter exists
$versions = isset($_GET['versions']);  // Check if 'versions' parameter exists

// If the 'versions' parameter is set, list all files in the 'xml/' directory, excluding the '.xml' extension
if ($versions) {
    $files = scandir('xml');  // Get all files in the 'xml' directory
    $versions_list = [];

    // Loop through the files and exclude '.' and '..' as well as files that don't end with '.xml'
    foreach ($files as $file) {
        if ($file !== '.' && $file !== '..' && strpos($file, '.xml') !== false) {
            // Remove the '.xml' extension and add the file name to the list
            $version = pathinfo($file, PATHINFO_FILENAME);
            
            // Remove the first letter/number from the version string
            $version = substr($version, 1);  // This removes the first character
            
            $versions_list[] = $version;
        }
    }

    // Output the list of versions in JSON format
    header('Content-Type: application/json');
    echo json_encode($versions_list);  // Send the list of versions as a JSON response
}

elseif ($xml) {
    $files = scandir('xml');  // Get all files in the 'xml' directory

    $xml_file = null;

    // Loop through the files and try to find a match, ignoring the first character of filenames
    foreach ($files as $file) {
        if ($file !== '.' && $file !== '..' && strpos($file, '.xml') !== false) {
            $filename_without_extension = pathinfo($file, PATHINFO_FILENAME);
            
            // Remove the first character from the file name
            $filename_without_extension = substr($filename_without_extension, 1);
            
            if ($filename_without_extension === $id) {
                $xml_file = "xml/{$file}";  // Set the matched XML file
                break;
            }
        }
    }

    // Check if the XML file was found
    if ($xml_file && file_exists($xml_file)) {
        // Load the XML content from the file
        $xml_content = file_get_contents($xml_file);

        // If 'self' parameter is present, modify the XML
        if ($hosted) {
            // Load the XML content into a SimpleXMLElement object
            $xml_object = simplexml_load_string($xml_content);

            // Modify the <Add> element to include the SourcePath and AllowCdnFallback attributes
            $add_element = $xml_object->Add;

            // Dynamically set the SourcePath to include the id, ensuring spaces are replaced with '%20'
            $encoded_id = urlencode($id);  // This will replace spaces with '+' and other special characters
            $encoded_id = str_replace('+', '%20', $encoded_id); // Replace '+' with '%20'
            $protocol = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
            $current_host = $protocol . '://' . $_SERVER['HTTP_HOST'];
            $add_element->addAttribute('SourcePath', $current_host . '/kms/office/versions/' . $encoded_id . '/');
            $add_element->addAttribute('AllowCdnFallback', 'TRUE');

            // Convert the modified XML back to a string
            $xml_content = $xml_object->asXML();
        }

        // Set the content type to XML
        header('Content-Type: application/xml');
        echo $xml_content;  // Output the (modified) content of the XML file
    } else {
        http_response_code(404);  // If the XML file does not exist, return 404
    }
} 
// If the 'hosted' parameter is set, list all folder names in the 'versions/' directory
elseif ($hosted) {
    // If an 'id' is provided, check if it exists as a directory in 'versions/'
    if ($id) {
        if (is_dir('versions/' . $id)) {
            echo 'true';  // Return 'true' if the directory exists
        } else {
            echo 'false';  // Return 'false' if the directory does not exist
        }
    } else {
        // If no 'id' is provided, list all folder names in the 'versions/' directory
        $folders = scandir('versions');  // Get all files and directories in the 'versions' directory
        $folder_list = [];

        // Loop through and filter out files, keep only directories (excluding '.' and '..')
        foreach ($folders as $folder) {
            if ($folder !== '.' && $folder !== '..' && is_dir('versions/' . $folder)) {
                $folder_list[] = $folder;  // Add directory names to the list
            }
        }

        // Output the list of folder names in JSON format
        header('Content-Type: application/json');
        echo json_encode($folder_list);  // Send the list of folders as a JSON response
    }
}
// If the 'xml' parameter is set, load the corresponding XML file

// Otherwise, load the data from the JSON file
else {
    $data = json_decode(file_get_contents('data.json'), true);

    // Check if the ID exists in the JSON data
    if ($id && isset($data[$id])) {
        echo $data[$id];  // Display the text from the corresponding section
    } else {
        http_response_code(404);  // If the ID does not exist, return 404
    }
}
?>
