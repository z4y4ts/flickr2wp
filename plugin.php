<?php
/*
Plugin Name: Flickr to Wordpress custom templates
Version: 0.1
Description: Lets you customize layout of photo posts shared from Flickr and make it a draft post.
Plugin URI: http://github.com/z4y4ts/flickr2wp-custom-templates/
Author: Alexander Zayats
Author URI: http://zayats.org.ua/
License: GPL
*/

function call_python_subprocess($input) {
    $descriptorspec = array(
       0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
       1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
       2 => array("file", "/tmp/error-output.txt", "a") // stderr is a file to write to
    );

    $cwd = plugin_dir_path(__FILE__);
    // $env = array('some_option' => 'aeiou');

    $process = proc_open('python flickr2wp_worker.py', $descriptorspec, $pipes, $cwd);

    if (!is_resource($process)) {
        return $input;
    }
    // $pipes now looks like this:
    // 0 => writeable handle connected to child stdin
    // 1 => readable handle connected to child stdout
    // Any error output will be appended to /tmp/error-output.txt

    fwrite($pipes[0], $input);
    fclose($pipes[0]);

    $output = stream_get_contents($pipes[1]);
    fclose($pipes[1]);

    // It is important that you close any pipes before calling
    // proc_close in order to avoid a deadlock
    proc_close($process);
    return $output;
}

function flickr_custom_layout($post_body) {
    if ($_SERVER['HTTP_USER_AGENT'] != 'Flickr') {
        return $post_body;
    }

    $processed_body = call_python_subprocess($post_body);

    return $processed_body;

}

function flickr_draft_post( $post_status ) {
    if($_SERVER['HTTP_USER_AGENT'] == 'Flickr') {
        return 'draft';
    } else {
        return $post_status;
    }
}

add_filter('status_save_pre', 'flickr_draft_post');
add_filter('content_save_pre', 'flickr_custom_layout');
?>
