import 'package:flutter/material.dart';

class Sidebar extends StatelessWidget {
  const Sidebar({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
        child: ListView(
      padding: EdgeInsets.zero,
      children: const [
        SizedBox(height: 100),
        ListTile(
          leading: Icon(Icons.person),
          title: Text('Profile'),
        ),
        ListTile(
          leading: Icon(Icons.settings),
          title: Text('Paramètre'),
        ),
        ListTile(
          leading: Icon(Icons.notifications),
          title: Text('Notification'),
        ),
        SizedBox(height: 300),
        ListTile(
          leading: Icon(Icons.logout),
          title: Text('Déconnexion'),
        ),
      ],
    ));
  }
}
