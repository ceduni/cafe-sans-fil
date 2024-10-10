import 'dart:ui';

import 'package:app/config.dart';
import 'package:app/provider/cafe_provider.dart';
import 'package:app/provider/language_provider.dart';
import 'package:app/provider/order_provider.dart';
import 'package:app/provider/period_selector_provider.dart';
import 'package:app/provider/shift_provider.dart';
import 'package:app/provider/stock_provider.dart';
import 'package:app/provider/volunteer_provider.dart';
import 'package:app/screens/main%20screens/article.dart';
import 'package:app/screens/main%20screens/benevole.dart';
import 'package:app/screens/main%20screens/dashboard.dart';
import 'package:app/screens/main%20screens/horaire.dart';
import 'package:app/screens/setting%20options/settings_page.dart';
import 'package:flutter/material.dart';
import 'package:app/l10n/l10n.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';
import 'package:provider/provider.dart';
import 'package:app/provider/auth_provider.dart';
import 'package:app/screens/Login/login_page.dart';
import 'package:app/provider/message_provider.dart';
import 'package:app/screens/messages/message_home_page.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => LanguageProvider()),
        ChangeNotifierProvider(create: (context) => PeriodSelectorProvider()),
        ChangeNotifierProvider(create: (context) => OrderProvider()),
        ChangeNotifierProvider(create: (context) => StockProvider()),
        ChangeNotifierProvider(create: (context) => ShiftProvider()),
        ChangeNotifierProvider(create: (context) => VolunteerProvider()),
        ChangeNotifierProvider(create: (context) => CafeProvider()),
        ChangeNotifierProvider(create: (context) => AuthProvider()),
        ChangeNotifierProvider(create: (context) => MessageProvider()),
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
          home: const LoginPage(),
          routes: {
            '/settings': (context) => const SettingsPage(),
            '/home': (context) => const RootPage(),
            '/login': (context) => const LoginPage(),
            '/messages': (context) => MessageHomePage(),
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
  int currentPage = 1;
  List<Widget> pages = [
    // barre de navigation
    const Benevole(),
    const Dashboard(),
    const Horaire(),
    const Article(),
    //MessageHomePage()
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
          /*const NavigationDestination(
              icon: Icon(
                Icons.message,
                color: Colors.white,
              ),
              label: "Messages"),*/
        ],
        onDestinationSelected: (int index) {
          setState(() {
            currentPage = index;
          });
        },
        selectedIndex: currentPage,
        backgroundColor: Config.specialBlue,
      ),
    );
  }
}
