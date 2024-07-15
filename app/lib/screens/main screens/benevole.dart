import 'package:app/screens/side%20bar/side_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localization.dart';

class Benevole extends StatelessWidget {
   Benevole({super.key});
  List<Map<String,String>> volunteers = [
    {'image':'images/volunteer1.jpg','name':'John Doe'},
    {'image':'images/volunteer2.jpg','name':'pauline Uvier'},
    {'image':'images/volunteer3.jpg','name':'paul van ingh'},
    {'image':'images/volunteer4.jpg','name':'Laurie campion'}
  ];
    

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: const Sidebar(),
      appBar: AppBar(
        title: Text(AppLocalizations.of(context)!.pagesTitles_volunteerTitle),
        surfaceTintColor: const Color.fromARGB(255, 138, 199, 249),
      ),
      body:Padding(
        
        padding: const EdgeInsets.all(16.0),
        child: 
          SingleChildScrollView(
              child: Column(
                  children: [
                    for (var volunteer in volunteers)
                       
                      Column(
                        children: [
                          ListTile(
                            leading: CircleAvatar(
                              backgroundImage: AssetImage(volunteer['image']!),
                            ),
                            title: Text(volunteer['name']!),
                            subtitle: const Text('Volunteer'),
                            onTap: () {
                              // Navigate to the volunteer's profile
                            },
                            
                          ),
                          const Divider()
                        ],
                      ),
                      
                  ],
              ),
          ), 
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
