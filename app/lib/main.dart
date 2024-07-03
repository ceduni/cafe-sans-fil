import 'package:app/provider/language_provider.dart';
import 'package:app/bottom%20navigation%20bar/article.dart';
import 'package:app/bottom%20navigation%20bar/benevole.dart';
import 'package:app/bottom%20navigation%20bar/dashboard.dart';
import 'package:app/bottom%20navigation%20bar/evenement.dart';
import 'package:app/bottom%20navigation%20bar/horaire.dart';
import 'package:app/side%20bar/setting%20options/settings_page.dart';
import 'package:flutter/material.dart';
import 'package:app/l10n/l10n.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';
import 'package:provider/provider.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => LanguageProvider()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<LanguageProvider>(
      builder: (context, languageProvider, child) {
        return MaterialApp(
          theme: ThemeData(
            brightness: Brightness.light,
            primaryColor: const Color.fromARGB(255, 138, 199, 249),
          ),
          supportedLocales: L10n.all,
          locale: languageProvider.getactualLanguage(), //en, fr or es  language
          localizationsDelegates: AppLocalizations.localizationsDelegates,
          debugShowCheckedModeBanner: false,
          home: const RootPage(),
          routes: {
            '/settings': (context) => const SettingsPage(),
          },
        );
      },
    );
  }
}

class RootPage extends StatefulWidget {
  const RootPage({super.key});

  @override
  State<RootPage> createState() => _RootPageState();
}

class _RootPageState extends State<RootPage> {
  int currentPage = 2;
  List<Widget> pages = const [
    // barre de navigation
    Benevole(),
    Evenement(),
    Dashboard(),
    Horaire(),
    Article(),
  ];
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: pages[currentPage], //const Dashboard(),
      bottomNavigationBar: NavigationBar(
        destinations: [
          NavigationDestination(
            icon: const Icon(
              Icons.volunteer_activism,
              color: Colors.white,
            ),
            label: AppLocalizations.of(context)!
                .bottomNavigationBar_volunteerButtonText,
          ),
          NavigationDestination(
            icon: const Icon(
              Icons.event,
              color: Colors.white,
            ),
            label: AppLocalizations.of(context)!
                .bottomNavigationBar_eventButtonText,
          ),
          NavigationDestination(
            icon: const Icon(
              Icons.dashboard,
              color: Colors.white,
            ),
            label: AppLocalizations.of(context)!
                .bottomNavigationBar_dashboardButtonText,
          ),
          NavigationDestination(
            icon: const Icon(
              Icons.access_time,
              color: Colors.white,
            ),
            label: AppLocalizations.of(context)!
                .bottomNavigationBar_hourlyButtonText,
          ),
          NavigationDestination(
            icon: const Icon(
              Icons.article,
              color: Colors.white,
            ),
            label: AppLocalizations.of(context)!
                .bottomNavigationBar_articleButtonText,
          ),
        ],
        onDestinationSelected: (int index) {
          setState(() {
            currentPage = index;
          });
        },
        selectedIndex: currentPage,
        backgroundColor: const Color.fromARGB(255, 138, 199, 249),
      ),
    );
  }
}
