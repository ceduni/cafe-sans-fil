import 'package:app/modeles/Volunteer.dart';
import 'package:app/screens/side%20bar/side_bar.dart';
import 'package:app/services/VolunteerService.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';

class Benevole extends StatefulWidget {
   const Benevole({super.key});

  @override
  State<Benevole> createState() => _BenevoleState();
}

class _BenevoleState extends State<Benevole> {
   List <Volunteer> volunteers1 = [];
   bool isLoading = true;
   final volunteerService = Volunteerservice();

  List<Map<String,String>> volunteers = [
    {'image':'images/volunteer1.jpg','name':'John Doe'},
    {'image':'images/volunteer2.jpg','name':'pauline Uvier'},
    {'image':'images/volunteer3.jpg','name':'paul van ingh'},
    {'image':'images/volunteer4.jpg','name':'Laurie campion'}
  ];

  @override
  void initState() {
    super.initState();
    // Fetch the volunteers from the database
    fetch();
  }

  Future<void> fetch() async {
    // Fetch the volunteers from the database
    try{
      List<Volunteer> vol = await volunteerService.fetchVolunteers();
      setState(() {
        volunteers1 = vol;
        isLoading = false;
      });
    }
    catch(e){
      isLoading = false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.pagesTitles_volunteerTitle),
        surfaceTintColor: const Color.fromARGB(255, 138, 199, 249),
      ),
      body: isLoading
          ? const Center(
              child: CircularProgressIndicator(),
            )
          : ListView.builder(
              itemCount: volunteers1.length,
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      ListTile(
                        leading: CircleAvatar(
                          backgroundImage: NetworkImage(volunteers1[index].image),
                        ),
                        title: Text("${volunteers1[index].firstName} ${volunteers1[index].lastName}") ,
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
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Add a new volunteer
        },
        backgroundColor: const Color.fromARGB(255, 138, 199, 249),
        child: const Icon(
          Icons.add_outlined,
          color: Colors.white,
          

        ),
      ));
  }
}
