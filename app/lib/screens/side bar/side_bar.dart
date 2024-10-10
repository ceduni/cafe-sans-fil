import 'package:app/config.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';
import 'package:app/provider/auth_provider.dart';
import 'package:provider/provider.dart';

class Sidebar extends StatelessWidget {
  const Sidebar({super.key});

  @override
  Widget build(BuildContext context) {
    TextStyle style = const TextStyle(color: Colors.white);
    return Drawer(
      child: Container(
        color: Config.specialBlue,
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            const SizedBox(height: 100),
            ListTile(
              leading: const Icon(
                Icons.person,
                color: Colors.white,
              ),
              title: Text(
                AppLocalizations.of(context)!.sidebar_profile,
                style: style,
              ),
            ),
            ListTile(
              leading: const Icon(
                Icons.settings,
                color: Colors.white,
              ),
              title: Text(
                AppLocalizations.of(context)!.sidebar_setting,
                style: style,
              ),
              onTap: () {
                Navigator.pushNamed(context, '/settings');
              },
            ),
            ListTile(
              leading: const Icon(
                Icons.notifications,
                color: Colors.white,
              ),
              title: Text(
                AppLocalizations.of(context)!.sidebar_notification,
                style: style,
              ),
            ),
            const SizedBox(height: 300),
            ListTile(
              leading: const Icon(
                Icons.logout,
                color: Colors.white,
              ),
              title: Text(
                AppLocalizations.of(context)!.sidebar_logOut,
                style: style,
              ),
              onTap: () async {
                await Provider.of<AuthProvider>(context, listen: false)
                    .logout(); // Logout
                Navigator.pushNamedAndRemoveUntil(
                    context, '/login', (route) => false); // Redirect to login
              },
            ),
          ],
        ),
      ),
    );
  }
}
