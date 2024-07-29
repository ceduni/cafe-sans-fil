class Shift {
  final String id;
  final String cafeName;
  final String matricule;
  final List<ShiftDetail> shifts;

  Shift({
    required this.id,
    required this.cafeName,
    required this.matricule,
    required this.shifts,
  });

  factory Shift.fromJson(Map<String, dynamic> json) {
    var shiftList = json['shift'] as List;
    List<ShiftDetail> shiftDetailList =
        shiftList.map((i) => ShiftDetail.fromJson(i)).toList();

    return Shift(
      id: json['_id'],
      cafeName: json['cafe_name'],
      matricule: json['matricule'],
      shifts: shiftDetailList,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      '_id': {'\$oid': id},
      'cafe_name': cafeName,
      'matricule': matricule,
      'shift': shifts.map((shift) => shift.toJson()).toList(),
    };
  }
}

class ShiftDetail {
  final DateTime date;
  final String startTime;
  final String endTime;

  ShiftDetail({
    required this.date,
    required this.startTime,
    required this.endTime,
  });

  factory ShiftDetail.fromJson(Map<String, dynamic> json) {
    return ShiftDetail(
      date: DateTime.parse(json['date']),
      startTime: json['startTime'],
      endTime: json['endTime'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'date': date.toIso8601String(),
      'startTime': startTime,
      'endTime': endTime,
    };
  }
}
