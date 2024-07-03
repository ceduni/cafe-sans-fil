import 'package:app/provider/language_provider.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';
import 'package:provider/provider.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        surfaceTintColor: Colors.blue,
        title: Text(
          AppLocalizations.of(context)!.sidebar_setting,
        ),
        leading: IconButton(
          onPressed: () {
            Navigator.pop(context);
          },
          icon: const Icon(Icons.arrow_back_ios),
        ),
      ),
      body: Column(
        children: [
          PopupMenuButton<Locale>(
            // this widget is used for changing the language of the app
            onSelected: (Locale newLocale) {
              context
                  .read<LanguageProvider>()
                  .changeLanguague(newLanguage: newLocale);
            },
            itemBuilder: (BuildContext context) => <PopupMenuEntry<Locale>>[
              const PopupMenuItem<Locale>(
                value: Locale('fr', 'FR'),
                child: Text('Français'),
              ),
              const PopupMenuItem<Locale>(
                value: Locale('es', 'ES'),
                child: Text('Español'),
              ),
              const PopupMenuItem<Locale>(
                value: Locale('en', 'US'),
                child: Text('English'),
              ),
            ],
            child: Container(
              width: double.infinity,
              decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(100)),
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const SizedBox(width: 15),
                    const Icon(
                      Icons.language,
                      color: Colors.blue,
                    ),
                    const SizedBox(width: 10),
                    Text(
                      AppLocalizations.of(context)!.select_language_text,
                      style: const TextStyle(fontSize: 20),
                    ),
                  ],
                ),
              ),
            ),
          )
        ],
      ),
    );
  }
}
