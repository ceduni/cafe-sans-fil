import 'package:app/bottom%20navigation%20bar/article.dart';
import 'package:app/bottom%20navigation%20bar/benevole.dart';
import 'package:app/bottom%20navigation%20bar/dashboard.dart';
import 'package:app/bottom%20navigation%20bar/evenement.dart';
import 'package:app/bottom%20navigation%20bar/horaire.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        brightness: Brightness.light,
        primaryColor: const Color.fromARGB(255, 138, 199, 249),
      ),
      debugShowCheckedModeBanner: false,
      home: const RootPage(),
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
        destinations: const [
          NavigationDestination(
            icon: Icon(
              Icons.volunteer_activism,
              color: Colors.white,
            ),
            label: 'Bénévole',
          ),
          NavigationDestination(
            icon: Icon(
              Icons.event,
              color: Colors.white,
            ),
            label: 'Evènement',
          ),
          NavigationDestination(
            icon: Icon(
              Icons.dashboard,
              color: Colors.white,
            ),
            label: 'Dashbord',
          ),
          NavigationDestination(
            icon: Icon(
              Icons.access_time,
              color: Colors.white,
            ),
            label: 'Horaire',
          ),
          NavigationDestination(
            icon: Icon(
              Icons.article,
              color: Colors.white,
            ),
            label: 'Article',
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
