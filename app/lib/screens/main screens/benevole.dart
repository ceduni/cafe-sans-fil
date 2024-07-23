import 'package:app/provider/volunteer_provider.dart';
import 'package:app/screens/side%20bar/side_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';
import 'package:provider/provider.dart';

class Benevole extends StatefulWidget {
  const Benevole({super.key});

  @override
  State<Benevole> createState() => _BenevoleState();
}

class _BenevoleState extends State<Benevole> {
  List<Map<String, String>> volunteers = [
    {'image': 'images/volunteer1.jpg', 'name': 'John Doe'},
    {'image': 'images/volunteer2.jpg', 'name': 'pauline Uvier'},
    {'image': 'images/volunteer3.jpg', 'name': 'paul van ingh'},
    {'image': 'images/volunteer4.jpg', 'name': 'Laurie campion'}
  ];

  @override
  void initState() {
    super.initState();
    fetch();
  }

  Future<void> fetch() async {
    // Fetch the volunteers from the database
    await Provider.of<VolunteerProvider>(context, listen: false)
        .fetchVolunteer();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.pagesTitles_volunteerTitle),
        surfaceTintColor: const Color.fromARGB(255, 138, 199, 249),
      ),
      body: Consumer<VolunteerProvider>(
        builder: (context, volunteerProvider, child) {
          if (volunteerProvider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          } else if (volunteerProvider.hasError) {
            return Center(
                child: Text('Error: ${volunteerProvider.errorMessage}'));
          } else {
            return Center(
              child: ListView.builder(
                itemCount:
                    (context.read<VolunteerProvider>().Volunteers).length,
                itemBuilder: (context, index) {
                  return Padding(
                    padding: const EdgeInsets.all(3.0),
                    child: Column(
                      children: [
                        ListTile(
                          leading: CircleAvatar(
                            backgroundImage: NetworkImage((context
                                    .read<VolunteerProvider>()
                                    .Volunteers)[index]
                                .photoUrl),
                          ),
                          title: Text(
                              "${(context.read<VolunteerProvider>().Volunteers)[index].firstName} "),
                          subtitle: const Text("volunteer"),
                          onTap: () {
                            // Open the volunteer details page
                          },
                        ),
                        const Divider(),
                      ],
                    ),
                  );
                },
              ),
            );
          }
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Add a new volunteer
        },
        backgroundColor: const Color.fromARGB(255, 138, 199, 249),
        child: const Icon(
          Icons.add_outlined,
          color: Colors.white,
        ),
      ),
    );
  }
}
