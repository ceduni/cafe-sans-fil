import 'package:flutter/material.dart';

class Sidebar extends StatelessWidget {
  const Sidebar({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      backgroundColor: const Color.fromARGB(255, 138, 199, 249),
      child: ListView(
      padding: EdgeInsets.zero,
      children: const [
        SizedBox(height: 100),
        ListTile(
          leading: Icon(
            Icons.person,
            color: Colors.white,
            ),
          title: Text(
                    'Profile',
                    style: TextStyle(color:Colors.white),
                    ),
        ),
        ListTile(
          leading: Icon(
            Icons.settings,
            color: Colors.white,
            ),
          title: Text(
                      'Paramètre',
                      style: TextStyle(color:Colors.white),
                      ),
        ),
        ListTile(
          leading: Icon(
                    Icons.notifications,
                    color: Colors.white,
                    ),
          title: Text(
                      'Notification',
                      style: TextStyle(color:Colors.white),
                      ),
        ),
        SizedBox(height: 300),
        ListTile(
          leading: Icon(
                      Icons.logout,
                      color: Colors.white,
                      ),
          title: Text(
            'Déconnexion',
            style: TextStyle(color:Colors.white),
            ),
        ),
      ],
    ));
  }
}
