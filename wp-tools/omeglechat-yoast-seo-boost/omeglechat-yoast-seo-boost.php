<?php
/**
 * Plugin Name: OmegleChat Yoast SEO Boost
 * Description: Bulk Yoast SEO meta for imported posts + sitewide templates.
 * Version: 1.2.1
 * Author: OmegleChat
 */

if (!defined('ABSPATH')) {
    exit;
}

function oc_seo_len($text) {
    return function_exists('mb_strlen') ? mb_strlen($text) : strlen($text);
}

function oc_seo_sub($text, $start, $len = null) {
    if (function_exists('mb_substr')) {
        return $len === null ? mb_substr($text, $start) : mb_substr($text, $start, $len);
    }
    return $len === null ? substr($text, $start) : substr($text, $start, $len);
}

function oc_seo_rpos($hay, $needle) {
    if (function_exists('mb_strrpos')) {
        return mb_strrpos($hay, $needle);
    }
    return strrpos($hay, $needle);
}

function oc_seo_lower($text) {
    return function_exists('mb_strtolower') ? mb_strtolower($text) : strtolower($text);
}

function oc_seo_clip($text, $max = 155) {
    $text = html_entity_decode(wp_strip_all_tags((string) $text), ENT_QUOTES, 'UTF-8');
    $text = preg_replace('/\s+/u', ' ', trim($text));
    if ($text === null) { $text = ''; }
    if (oc_seo_len($text) <= $max) { return $text; }
    $cut = oc_seo_sub($text, 0, $max - 1);
    $sp = oc_seo_rpos($cut, ' ');
    if ($sp !== false && $sp > 40) { $cut = oc_seo_sub($cut, 0, $sp); }
    return rtrim($cut, '.,;:-') . '...';
}

function oc_seo_starts($hay, $needle) {
    return strpos($hay, $needle) === 0;
}

function oc_seo_focus_keyphrase($post) {
    $title = get_the_title($post);
    $title = preg_replace('/\s+[—–-]\s+Late Bloom Stories Part .*$/iu', '', $title);
    $title = preg_replace('/\s+[—–-]\s+The Quiet Hours.*$/iu', '', $title);
    $title = preg_replace('/\s+[—–-]\s+OmegleChat.*$/iu', '', $title);
    $title = trim((string) $title);
    $slug = (string) $post->post_name;
    $map = array(
        'best-websites-to-talk-to-strangers-2026' => 'websites to talk to strangers',
        'free-random-chat-online' => 'free random chat online',
        'omegle-alternative-2026' => 'omegle alternatives',
        'omegle-vs-alternatives-2026' => 'omegle vs alternatives',
        'random-chat-safety-2026' => 'random chat safety',
        'make-friends-random-chat' => 'make friends random chat',
        'what-true-love-actually-means' => 'what true love means',
        'why-older-adults-talk-less-as-they-age' => 'why older adults talk less',
        'what-was-omegle' => 'what was omegle',
        'ometv-not-working-alternatives' => 'ometv not working',
        'language-exchange-strangers' => 'language exchange strangers',
    );
    if (isset($map[$slug])) { return $map[$slug]; }
    if (oc_seo_starts($slug, 'late-bloom-')) { return 'late bloom love story'; }
    if (oc_seo_starts($slug, 'quiet-hours-')) { return 'quiet hours chronicle'; }
    if (oc_seo_starts($slug, 'stranger-scripts-')) { return 'what to say to strangers'; }
    $words = preg_split('/\s+/u', oc_seo_lower($title));
    $stop = array('the','and','for','with','from','that','this','your','you','are','was');
    $keep = array();
    foreach ((array) $words as $w) {
        if (oc_seo_len($w) > 2 && !in_array($w, $stop, true)) { $keep[] = $w; }
    }
    return oc_seo_clip(implode(' ', array_slice($keep, 0, 5)), 60);
}

function oc_seo_metadesc($post) {
    $excerpt = (string) $post->post_excerpt;
    if ($excerpt === '') { $excerpt = (string) $post->post_content; }
    $desc = oc_seo_clip($excerpt, 155);
    if ($desc === '') {
        $desc = oc_seo_clip(get_the_title($post) . ' — guidance from OmegleChat Blog.', 155);
    }
    return $desc;
}

function oc_seo_seo_title($post) {
    return oc_seo_clip(get_the_title($post), 50) . ' | OmegleChat Blog';
}

function oc_seo_apply_post($post_id, $force = false) {
    $post = get_post($post_id);
    if (!$post || $post->post_type !== 'post') { return false; }
    $changed = false;
    $pairs = array(
        '_yoast_wpseo_metadesc' => oc_seo_metadesc($post),
        '_yoast_wpseo_focuskw' => oc_seo_focus_keyphrase($post),
        '_yoast_wpseo_title' => oc_seo_seo_title($post),
    );
    foreach ($pairs as $key => $val) {
        $cur = (string) get_post_meta($post_id, $key, true);
        if ($force || $cur === '') {
            if ($cur !== $val) {
                update_post_meta($post_id, $key, $val);
                $changed = true;
            }
        }
    }
    if ($post->post_status === 'publish') {
        $robots = get_post_meta($post_id, '_yoast_wpseo_meta-robots-noindex', true);
        if ((string) $robots === '1') {
            delete_post_meta($post_id, '_yoast_wpseo_meta-robots-noindex');
            $changed = true;
        }
    }
    return $changed;
}

function oc_seo_apply_sitewide() {
    update_option('blogdescription', 'True love, marriage wisdom, Late Bloom stories, and safe random-chat guides from OmegleChat.');
    $titles = get_option('wpseo_titles');
    if (!is_array($titles)) { $titles = array(); }
    $titles['separator'] = 'sc-pipe';
    $titles['title-home-wpseo'] = 'OmegleChat Blog %%sep%% Love, connection & safe random chat guides';
    $titles['metadesc-home-wpseo'] = 'Practical love advice, Late Bloom romance stories, and safety-first guides to talk to strangers online — from OmegleChat.';
    $titles['title-post'] = '%%title%% %%sep%% OmegleChat Blog';
    $titles['metadesc-post'] = '%%excerpt%%';
    $titles['title-page'] = '%%title%% %%sep%% OmegleChat Blog';
    $titles['title-category'] = '%%term_title%% guides %%sep%% OmegleChat Blog';
    $titles['metadesc-category'] = 'Browse %%term_title%% articles on OmegleChat Blog — connection, love, and safer online conversation.';
    $titles['noindex-author'] = true;
    $titles['disable-author'] = true;
    $titles['company_or_person'] = 'company';
    $titles['company_name'] = 'OmegleChat';
    update_option('wpseo_titles', $titles);
    $social = get_option('wpseo_social');
    if (!is_array($social)) { $social = array(); }
    $social['facebook_site'] = 'https://omeglechat.online';
    update_option('wpseo_social', $social);
    $user = get_user_by('login', 'omegleadmin');
    if ($user) {
        wp_update_user(array(
            'ID' => $user->ID,
            'display_name' => 'Morgan Rivers',
            'nickname' => 'Morgan Rivers',
            'first_name' => 'Morgan',
            'last_name' => 'Rivers',
            'user_url' => 'https://blog.omeglechat.online',
            'description' => 'Staff essayist at OmegleChat Blog — writing about love, later-life connection, and safer stranger conversation.',
        ));
        update_user_meta($user->ID, 'wpseo_noindex_author', 'on');
    }
}

add_action('admin_menu', function () {
    add_management_page('OmegleChat SEO Boost', 'OmegleChat SEO Boost', 'manage_options', 'oc-yoast-seo-boost', 'oc_seo_admin_page');
});

function oc_seo_admin_page() {
    if (!current_user_can('manage_options')) { return; }
    $msg = '';
    $err = '';
    if (isset($_POST['oc_seo_run']) && check_admin_referer('oc_seo_run')) {
        try {
            @set_time_limit(300);
            $force = !empty($_POST['oc_seo_force']);
            oc_seo_apply_sitewide();
            $ids = get_posts(array(
                'post_type' => 'post',
                'post_status' => array('publish', 'future', 'draft'),
                'posts_per_page' => -1,
                'fields' => 'ids',
                'no_found_rows' => true,
            ));
            $updated = 0;
            foreach ($ids as $id) {
                if (oc_seo_apply_post((int) $id, $force)) { $updated++; }
            }
            delete_transient('wpseo_sitemap_cache_validator');
            $msg = sprintf('Done. Sitewide OK. Posts updated: %d / %d.', $updated, count($ids));
        } catch (Throwable $e) {
            $err = $e->getMessage();
        }
    }
    echo '<div class="wrap"><h1>OmegleChat Yoast SEO Boost</h1>';
    if ($msg) { echo '<div class="notice notice-success"><p>' . esc_html($msg) . '</p></div>'; }
    if ($err) { echo '<div class="notice notice-error"><p>' . esc_html($err) . '</p></div>'; }
    echo '<p>Fills Yoast SEO title, meta description, focus keyphrase; improves homepage templates; display name Morgan Rivers; noindex author archives.</p>';
    echo '<form method="post">';
    wp_nonce_field('oc_seo_run');
    echo '<p><label><input type="checkbox" name="oc_seo_force" value="1" checked> Overwrite existing Yoast title/desc/focus</label></p>';
    echo '<p><button class="button button-primary" name="oc_seo_run" value="1">Run SEO boost now</button></p>';
    echo '</form></div>';
}

add_action('save_post_post', function ($post_id) {
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) { return; }
    oc_seo_apply_post($post_id, false);
}, 20);
