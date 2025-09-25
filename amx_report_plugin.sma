#include <amxmodx>
#include <amxmisc>
#include <cstrike>
#include <fakemeta>

#define PLUGIN "CS Report System"
#define VERSION "1.0"
#define AUTHOR "Luci"

// Configurare
new g_WebhookURL[256]
new g_ServerName[64]
new g_ServerWebsite[128]

public plugin_init() {
    register_plugin(PLUGIN, VERSION, AUTHOR)
    
    // Comenzi pentru jucători
    register_clcmd("say /report", "cmd_report")
    register_clcmd("say_team /report", "cmd_report")
    
    // Comenzi pentru admini
    register_concmd("amx_report", "cmd_admin_report", ADMIN_LEVEL_A, "<nume> <motiv>")
    
    // Încarcă configurarea
    load_config()
}

public load_config() {
    new config_file[128]
    get_configsdir(config_file, charsmax(config_file))
    add(config_file, charsmax(config_file), "/report_config.ini")
    
    if(!file_exists(config_file)) {
        create_default_config(config_file)
    }
    
    // Încarcă setările
    new file = fopen(config_file, "rt")
    if(file) {
        new line[256], key[64], value[192]
        
        while(!feof(file)) {
            fgets(file, line, charsmax(line))
            trim(line)
            
            if(line[0] == ';' || line[0] == 0) continue
            
            if(parse(line, key, charsmax(key), value, charsmax(value))) {
                if(equal(key, "webhook_url")) {
                    copy(g_WebhookURL, charsmax(g_WebhookURL), value)
                }
                else if(equal(key, "server_name")) {
                    copy(g_ServerName, charsmax(g_ServerName), value)
                }
                else if(equal(key, "server_website")) {
                    copy(g_ServerWebsite, charsmax(g_ServerWebsite), value)
                }
            }
        }
        fclose(file)
    }
}

public create_default_config(const config_file[]) {
    new file = fopen(config_file, "wt")
    if(file) {
        fputs(file, "; Configurare Report System^n")
        fputs(file, "; URL-ul webhook-ului Discord^n")
        fputs(file, "webhook_url = http://localhost:5000/api/report^n")
        fputs(file, "; Numele serverului^n")
        fputs(file, "server_name = CS 1.6 Server^n")
        fputs(file, "; Website-ul serverului^n")
        fputs(file, "server_website = your-server.com^n")
        fclose(file)
    }
}

public cmd_report(id) {
    if(!is_user_connected(id)) return PLUGIN_HANDLED
    
    // Afișează meniul de raportare
    show_report_menu(id)
    return PLUGIN_HANDLED
}

public show_report_menu(id) {
    new menu = menu_create("Raportare Jucător", "report_menu_handler")
    
    // Adaugă jucătorii online
    new players[32], num
    get_players(players, num, "ch")
    
    for(new i = 0; i < num; i++) {
        new player_id = players[i]
        if(player_id == id) continue // Nu te poți raporta pe tine
        
        new name[32], steam_id[32]
        get_user_name(player_id, name, charsmax(name))
        get_user_authid(player_id, steam_id, charsmax(steam_id))
        
        new item_text[64]
        formatex(item_text, charsmax(item_text), "%s (%s)", name, steam_id)
        
        new item_data[8]
        num_to_str(player_id, item_data, charsmax(item_data))
        
        menu_additem(menu, item_text, item_data)
    }
    
    menu_setprop(menu, MPROP_EXIT, MEXIT_ALL)
    menu_display(id, menu, 0)
}

public report_menu_handler(id, menu, item) {
    if(item == MENU_EXIT) {
        menu_destroy(menu)
        return PLUGIN_HANDLED
    }
    
    new data[8], name[32], access, callback
    menu_item_getinfo(menu, item, access, data, charsmax(data), name, charsmax(name), callback)
    
    new reported_id = str_to_num(data)
    if(!is_user_connected(reported_id)) {
        client_print(id, print_chat, "[Report] Jucătorul nu mai este conectat!")
        menu_destroy(menu)
        return PLUGIN_HANDLED
    }
    
    // Salvează ID-ul jucătorului raportat
    set_user_info(id, "reported_player", data)
    
    // Afișează meniul cu motivele
    show_reason_menu(id)
    
    menu_destroy(menu)
    return PLUGIN_HANDLED
}

public show_reason_menu(id) {
    new menu = menu_create("Motivul Raportului", "reason_menu_handler")
    
    menu_additem(menu, "AIM HACK", "aim_hack")
    menu_additem(menu, "WALL HACK", "wall_hack")
    menu_additem(menu, "SPEED HACK", "speed_hack")
    menu_additem(menu, "BUNNY HOP", "bunny_hop")
    menu_additem(menu, "TEAM KILL", "team_kill")
    menu_additem(menu, "SPAM", "spam")
    menu_additem(menu, "INSULT", "insult")
    menu_additem(menu, "ALT MOTIV", "other")
    
    menu_setprop(menu, MPROP_EXIT, MEXIT_ALL)
    menu_display(id, menu, 0)
}

public reason_menu_handler(id, menu, item) {
    if(item == MENU_EXIT) {
        menu_destroy(menu)
        return PLUGIN_HANDLED
    }
    
    new data[32], name[32], access, callback
    menu_item_getinfo(menu, item, access, data, charsmax(data), name, charsmax(name), callback)
    
    new reported_id = str_to_num(get_user_info(id, "reported_player"))
    if(!is_user_connected(reported_id)) {
        client_print(id, print_chat, "[Report] Jucătorul nu mai este conectat!")
        menu_destroy(menu)
        return PLUGIN_HANDLED
    }
    
    // Trimite raportul
    send_report(id, reported_id, data)
    
    menu_destroy(menu)
    return PLUGIN_HANDLED
}

public send_report(reporter_id, reported_id, reason[]) {
    if(!is_user_connected(reporter_id) || !is_user_connected(reported_id)) {
        return
    }
    
    // Obține informațiile jucătorilor
    new reporter_name[32], reporter_steam_id[32]
    new reported_name[32], reported_steam_id[32]
    
    get_user_name(reporter_id, reporter_name, charsmax(reporter_name))
    get_user_authid(reporter_id, reporter_steam_id, charsmax(reporter_steam_id))
    
    get_user_name(reported_id, reported_name, charsmax(reported_name))
    get_user_authid(reported_id, reported_steam_id, charsmax(reported_steam_id))
    
    // Obține harta curentă
    new map_name[32]
    get_mapname(map_name, charsmax(map_name))
    
    // Obține informații suplimentare
    new additional_info[256]
    formatex(additional_info, charsmax(additional_info), 
             "Kills: %d | Deaths: %d | Ping: %dms", 
             get_user_frags(reported_id), 
             get_user_deaths(reported_id),
             get_user_ping(reported_id))
    
    // Trimite raportul prin HTTP
    send_http_report(reporter_name, reporter_steam_id, reported_name, reported_steam_id, 
                    reason, map_name, additional_info)
    
    // Confirmă jucătorului
    client_print(reporter_id, print_chat, "[Report] Raportul a fost trimis cu succes!")
    
    // Log pentru admini
    log_amx("Report: %s (%s) a raportat %s (%s) pentru %s", 
            reporter_name, reporter_steam_id, reported_name, reported_steam_id, reason)
}

public send_http_report(const reporter_name[], const reporter_steam_id[], 
                       const reported_name[], const reported_steam_id[], 
                       const reason[], const map_name[], const additional_info[]) {
    
    // Creează JSON-ul pentru raport
    new json_data[1024]
    formatex(json_data, charsmax(json_data),
             "{"
             "\"reporter_name\":\"%s\","
             "\"reporter_steam_id\":\"%s\","
             "\"reported_name\":\"%s\","
             "\"reported_steam_id\":\"%s\","
             "\"reason\":\"%s\","
             "\"map_name\":\"%s\","
             "\"additional_info\":\"%s\""
             "}",
             reporter_name, reporter_steam_id, reported_name, reported_steam_id,
             reason, map_name, additional_info)
    
    // Trimite prin HTTP către Vercel
    new url[256]
    formatex(url, charsmax(url), "%s/api/report", g_WebhookURL)
    
    // Folosește plugin-ul HTTP pentru AMX Mod X
    // Exemplu cu plugin-ul HTTP:
    // http_post(url, json_data, "http_response_handler")
    
    // Pentru implementare completă, instalează plugin-ul HTTP pentru AMX Mod X
    // și decomentează linia de mai sus
}

public cmd_admin_report(id, level, cid) {
    if(!cmd_access(id, level, cid, 3)) return PLUGIN_HANDLED
    
    new arg1[32], arg2[128]
    read_argv(1, arg1, charsmax(arg1))
    read_argv(2, arg2, charsmax(arg2))
    
    new target_id = cmd_target(id, arg1, CMDTARGET_OBEY_IMMUNITY)
    if(!target_id) return PLUGIN_HANDLED
    
    // Obține informațiile adminului
    new admin_name[32], admin_steam_id[32]
    get_user_name(id, admin_name, charsmax(admin_name))
    get_user_authid(id, admin_steam_id, charsmax(admin_steam_id))
    
    // Obține informațiile țintei
    new target_name[32], target_steam_id[32]
    get_user_name(target_id, target_name, charsmax(target_name))
    get_user_authid(target_id, target_steam_id, charsmax(target_steam_id))
    
    // Obține harta curentă
    new map_name[32]
    get_mapname(map_name, charsmax(map_name))
    
    // Trimite raportul
    send_http_report(admin_name, admin_steam_id, target_name, target_steam_id, 
                    arg2, map_name, "Raport administrativ")
    
    client_print(id, print_console, "[Report] Raport administrativ trimis pentru %s", target_name)
    
    return PLUGIN_HANDLED
}
