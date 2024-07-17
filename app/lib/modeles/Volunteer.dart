class Volunteer {
  final String firstName;
  final String lastName;
  final String image;

  Volunteer({required this.firstName,required this.lastName, required this.image});

  factory Volunteer.fromJson(Map<String, dynamic> json) {
    return Volunteer(
      firstName: json['first_name'],
      lastName: json['last_name'],
      image: json['photo_url'],
    );
  }
}