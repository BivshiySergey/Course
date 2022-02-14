#pragma once
#include <stdlib.h>
#include <iostream>
#include "include/httplib.h"
#include "include/nlohmann/json.hpp"
#include "mysql_connection.h"
#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/prepared_statement.h> 
using namespace std;
using json = nlohmann::json;

const string mysql_server = "localhost:3306";
const string mysql_username = "root";
const string mysql_password = "1111";
json lobby = json::array();

void authorization(const httplib::Request& req, httplib::Response& res);
void registration(const httplib::Request& req, httplib::Response& res);
void get_game(const httplib::Request& req, httplib::Response& res);
void set_game(const httplib::Request& req, httplib::Response& res);
void set_new_game(const httplib::Request& req, httplib::Response& res);
void get_new_game(const httplib::Request& req, httplib::Response& res);
void ratings(const httplib::Request& req, httplib::Response& res);
void delete_lobby(const httplib::Request& req, httplib::Response& res);
void delete_lobby_foo(int id);


int main()
{
	httplib::Server svr;

	svr.Post("/auth", authorization);
	svr.Post("/reg", registration);
	svr.Post("/get", get_game);
	svr.Post("/setgame", set_game);
	svr.Post("/setnew", set_new_game);
	svr.Post("/getnew", get_new_game);
	svr.Post("/ratings", ratings);
	svr.Post("/dellobby", delete_lobby);
	svr.listen("0.0.0.0", 5000);
}


void registration(const httplib::Request& req, httplib::Response& res)
{
	sql::Driver* driver;
	sql::Connection* con;
	sql::Statement* stmt;
	sql::PreparedStatement* pstmt;
	sql::ResultSet* result;
	string j_req = req.body.c_str();

	json j = json::parse(j_req);
	string login = j["login"], password = j["password"];
	try
	{
		driver = get_driver_instance();
		con = driver->connect(mysql_server, mysql_username, mysql_password);
	}
	catch (exception e)
	{
		std::cout << e.what() << std::endl;
		exit(1);
	}

	con->setSchema("players");
	stmt = con->createStatement();
	stmt->execute("CREATE TABLE IF NOT EXISTS `user`(id int AUTO_INCREMENT," \
		" name varchar(32) NOT NULL," \
		" password varchar(32) NOT NULL," \
		" rating int NOT NULL , PRIMARY KEY (id));");
	delete stmt;

	pstmt = con->prepareStatement("SELECT * FROM user;");
	result = pstmt->executeQuery();

	while (result->next()) {
		string result_str = result->getString(2);
		if (result_str == login)
		{
			res.set_content("Login exist", "text/plain");
			delete pstmt;
			delete con;
			return;
		}
	}


	pstmt = con->prepareStatement("INSERT INTO `user`(name, password,rating) VALUES(?,?,?)");
	pstmt->setString(1, login);
	pstmt->setString(2, password);
	pstmt->setInt(3, 150);
	pstmt->execute();

	delete pstmt;
	delete con;
	res.set_content("Registation succsess!", "text/plain");
}

void authorization(const httplib::Request& req, httplib::Response& res)
{
	sql::Driver* driver;
	sql::Connection* con;
	sql::PreparedStatement* pstmt;
	sql::ResultSet* result;

	json j = json::parse(req.body.c_str());
	try
	{
		driver = get_driver_instance();
		con = driver->connect(mysql_server, mysql_username, mysql_password);
	}
	catch (sql::SQLException e)
	{
		cout << "Could not connect to server. Error message: " << e.what() << endl;
		system("pause");
		exit(1);
	}
	con->setSchema("players");

	pstmt = con->prepareStatement("SELECT * FROM user;");
	result = pstmt->executeQuery();

	while (result->next()) {
		string result_login = result->getString(2), result_password = result->getString(3),
			login = j["login"], password = j["password"];
		if (result_login == login && result_password == password)
		{
			delete result;
			delete pstmt;
			delete con;
			res.set_content("authorized", "text/plain");
			return;
		}
	}
	res.set_content("Login or password is not correct", "text/plain");
	delete pstmt;
	delete con;
	return;
}

void ratings(const httplib::Request& req, httplib::Response& res)
{
	sql::Driver* driver;
	sql::Connection* con;
	sql::PreparedStatement* pstmt;
	sql::ResultSet* result;

	json j = json::parse(req.body.c_str());
	string winner = j["winner"], loser = j["loser"];
	int id = j["id"];
	try
	{
		driver = get_driver_instance();
		con = driver->connect(mysql_server, mysql_username, mysql_password);
	}
	catch (sql::SQLException e)
	{
		cout << "Could not connect to server. Error message: " << e.what() << endl;
		system("pause");
		exit(1);
	}
	con->setSchema("players");

	pstmt = con->prepareStatement("SELECT rating FROM user WHERE name = ?");
	pstmt->setString(1, winner);
	result = pstmt->executeQuery();
	int winner_rating = result->getInt(1);

	pstmt = con->prepareStatement("SELECT rating FROM user WHERE name = ?");
	pstmt->setString(1, loser);
	result = pstmt->executeQuery();
	int loser_rating = result->getInt(1);

	pstmt = con->prepareStatement("UPDATE `user` SET rating = ? WHERE name = ?");
	pstmt->setInt(1, winner_rating + 20);
	pstmt->setString(2, winner);
	pstmt->executeQuery();

	pstmt = con->prepareStatement("UPDATE `user` SET rating = ? WHERE name = ?");
	pstmt->setInt(1, loser_rating - 20);
	pstmt->setString(2, loser);
	pstmt->executeQuery();

	delete_lobby_foo(id);
	delete pstmt;
	delete con;
	return;
}

void delete_lobby(const httplib::Request& req, httplib::Response& res)
{
	json j = json::parse(req.body.c_str());
	int id = j["id"];
	if (lobby[id]["deleted"]) 
	{
		delete_lobby_foo(id);
	}
	else 
	{
		lobby[id]["deleted"] = true;
	}
	res.set_content("Lobby is deleted", "text/plain");
}

void delete_lobby_foo(int id)
{
	json new_lobby = json::array();
	for (int i = 0; i < lobby.size(); i++)
	{
		if (i > id) {
			lobby[i]["id"] = lobby[i]["id"] - 1;
		}
		if (i != id) {
			new_lobby.push_back(lobby[i]);
		}
	}
	lobby = new_lobby;
}

void set_new_game(const httplib::Request& req, httplib::Response& res)
{
	json j = json::parse(req.body.c_str());
	for (int i = 0; i < lobby.size(); i++)
	{
		if ((lobby[i]["name"] == j["name"] or j["name"]=="") and !lobby[i]["deleted"])
		{
			if (lobby[i]["new_player"]) {
				res.set_content(lobby[i].dump(), "text/json");
				return;
			}
			else
			{
				res.set_content("wait", "text/plain");
				return;
			}
		}
	}
	lobby.push_back(j);
	res.set_content("wait", "text/plain");
}
void get_new_game(const httplib::Request& req, httplib::Response& res)
{
	json j = json::parse(req.body.c_str());
	string search_name = j["search"];
	for (int i = 0; i < lobby.size(); i++)
	{
		string host_name = lobby[i]["name"];
		if (host_name == search_name or search_name == "")
		{
			if (!lobby[i]["new_player"] and !lobby[i]["deleted"]) {
				lobby[i]["new_player"] = true;
				lobby[i]["id"] = i;
				lobby[i]["enemy"] = j["name"];
				lobby[i]["deleted"] = false;
				lobby[i]["turn"] = false;
				string str = lobby[i].dump();
				res.set_content(str, "text/json");
				return;
			}
		}
	}
	res.set_content("wait", "text/plain");
}
void get_game(const httplib::Request& req, httplib::Response& res)
{
	json j = json::parse(req.body.c_str());
	int id = j["id"];
	bool turn = lobby[id]["turn"];
	if (turn)
	{
		lobby[id]["turn"] = false;
		string str = lobby[id].dump();
		res.set_content(str, "text/json");
		return;
	}
	res.set_content("waiting enemy turn", "text/plain");
}
void set_game(const httplib::Request& req, httplib::Response& res)
{
	json j = json::parse(req.body.c_str());
	int id = j["id"];
	lobby[id]["moves"] = j["moves"];
	lobby[id]["turn"] = true;
	res.set_content("game is set", "text/plain");
}