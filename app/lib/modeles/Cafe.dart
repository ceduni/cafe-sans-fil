import 'dart:convert';
import 'dart:typed_data';

class Cafe {
  final String id;
  final String cafeId;
  final String name;
  final String slug;
  final List<String> previousSlugs;
  final String description;
  final String imageUrl;
  final String faculty;
  final bool isOpen;
  final String? statusMessage;
  final List<OpeningHours> openingHours;
  final Location location;
  final Contact contact;
  final List<SocialMedia> socialMedia;
  final List<PaymentMethod> paymentMethods;
  final List<AdditionalInfo> additionalInfo;
  final List<Staff> staff;
  final List<MenuItem> menuItems;

  Cafe({
    required this.id,
    required this.cafeId,
    required this.name,
    required this.slug,
    required this.previousSlugs,
    required this.description,
    required this.imageUrl,
    required this.faculty,
    required this.isOpen,
    this.statusMessage,
    required this.openingHours,
    required this.location,
    required this.contact,
    required this.socialMedia,
    required this.paymentMethods,
    required this.additionalInfo,
    required this.staff,
    required this.menuItems,
  });

  factory Cafe.fromJson(Map<String, dynamic> json) {
    var idBuffer = json['cafe_id']['data'] as List<dynamic>;
    Uint8List idBytes =
        Uint8List.fromList(idBuffer.map((i) => i as int).toList());
    String cafeId = base64.encode(idBytes); // Convertir en base64 si nécessaire

    return Cafe(
      id: json['_id'],
      cafeId: cafeId,
      name: json['name'],
      slug: json['slug'],
      previousSlugs: List<String>.from(json['previous_slugs']),
      description: json['description'],
      imageUrl: json['image_url'],
      faculty: json['faculty'],
      isOpen: json['is_open'],
      statusMessage: json['status_message'],
      openingHours: (json['opening_hours'] as List)
          .map((e) => OpeningHours.fromJson(e))
          .toList(),
      location: Location.fromJson(json['location']),
      contact: Contact.fromJson(json['contact']),
      socialMedia: (json['social_media'] as List)
          .map((e) => SocialMedia.fromJson(e))
          .toList(),
      paymentMethods: (json['payment_methods'] as List)
          .map((e) => PaymentMethod.fromJson(e))
          .toList(),
      additionalInfo: (json['additional_info'] as List)
          .map((e) => AdditionalInfo.fromJson(e))
          .toList(),
      staff: (json['staff'] as List).map((e) => Staff.fromJson(e)).toList(),
      menuItems: (json['menu_items'] as List)
          .map((e) => MenuItem.fromJson(e))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    Uint8List idBytes = base64.decode(cafeId);
    List<int> idBuffer = idBytes.toList();
    return {
      '_id': {'\$oid': id},
      'cafe_id': {
        'type': 'Buffer',
        'data': idBuffer,
      },
      'name': name,
      'slug': slug,
      'previous_slugs': previousSlugs,
      'description': description,
      'image_url': imageUrl,
      'faculty': faculty,
      'is_open': isOpen,
      'status_message': statusMessage,
      'opening_hours': openingHours.map((e) => e.toJson()).toList(),
      'location': location.toJson(),
      'contact': contact.toJson(),
      'social_media': socialMedia.map((e) => e.toJson()).toList(),
      'payment_methods': paymentMethods.map((e) => e.toJson()).toList(),
      'additional_info': additionalInfo.map((e) => e.toJson()).toList(),
      'staff': staff.map((e) => e.toJson()).toList(),
      'menu_items': menuItems.map((e) => e.toJson()).toList(),
    };
  }
}

class OpeningHours {
  final String day;
  final List<TimeBlock> blocks;

  OpeningHours({required this.day, required this.blocks});

  factory OpeningHours.fromJson(Map<String, dynamic> json) {
    return OpeningHours(
      day: json['day'],
      blocks:
          (json['blocks'] as List).map((e) => TimeBlock.fromJson(e)).toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'day': day,
      'blocks': blocks.map((e) => e.toJson()).toList(),
    };
  }
}

class TimeBlock {
  final String start;
  final String end;

  TimeBlock({required this.start, required this.end});

  factory TimeBlock.fromJson(Map<String, dynamic> json) {
    return TimeBlock(
      start: json['start'],
      end: json['end'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'start': start,
      'end': end,
    };
  }
}

class Location {
  final String pavillon;
  final String local;
  final String id;

  Location({required this.pavillon, required this.local, required this.id});

  factory Location.fromJson(Map<String, dynamic> json) {
    return Location(
      pavillon: json['pavillon'],
      local: json['local'],
      id: json['_id'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'pavillon': pavillon,
      'local': local,
      '_id': {'\$oid': id},
    };
  }
}

class Contact {
  final String email;
  final String? phoneNumber;
  final String? website;
  final String? id;

  Contact({
    required this.email,
    required this.phoneNumber,
    required this.website,
    required this.id,
  });

  factory Contact.fromJson(Map<String, dynamic> json) {
    return Contact(
      email: json['email'],
      phoneNumber: json['phone_number'],
      website: json['website'],
      id: json['_id'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'phone_number': phoneNumber,
      'website': website,
      '_id': {'\$oid': id},
    };
  }
}

class SocialMedia {
  final String platformName;
  final String link;

  SocialMedia({required this.platformName, required this.link});

  factory SocialMedia.fromJson(Map<String, dynamic> json) {
    return SocialMedia(
      platformName: json['platform_name'],
      link: json['link'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'platform_name': platformName,
      'link': link,
    };
  }
}

class PaymentMethod {
  final String method;
  final double minimum;

  PaymentMethod({required this.method, required this.minimum});

  factory PaymentMethod.fromJson(Map<String, dynamic> json) {
    return PaymentMethod(
      method: json['method'],
      minimum: double.parse(json['minimum']['\$numberDecimal']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'method': method,
      'minimum': {'\$numberDecimal': minimum.toString()},
    };
  }
}

class AdditionalInfo {
  final String id;
  final String type;
  final String value;
  final DateTime start;
  final DateTime? end;

  AdditionalInfo({
    required this.id,
    required this.type,
    required this.value,
    required this.start,
    this.end,
  });

  factory AdditionalInfo.fromJson(Map<String, dynamic> json) {
    return AdditionalInfo(
      id: json['_id'],
      type: json['type'],
      value: json['value'],
      start: DateTime.parse(json['start']),
      end: json['end'] != null ? DateTime.parse(json['end']) : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      '_id': id,
      'type': type,
      'value': value,
      'start': start.toIso8601String(),
      'end': end?.toIso8601String(),
    };
  }
}

class Staff {
  final String id;
  final String username;
  final String role;

  Staff({required this.id, required this.username, required this.role});

  factory Staff.fromJson(Map<String, dynamic> json) {
    return Staff(
      id: json['_id'],
      username: json['username'],
      role: json['role'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      '_id': {'\$oid': id},
      'username': username,
      'role': role,
    };
  }
}

class MenuItem {
  final String id;
  final List<int> itemId; // Pour le Buffer, utiliser une liste d'entiers
  final String name;
  final String slug;
  final List<String> tags;
  final String description;
  final String imageUrl;
  final double price;
  final bool inStock;
  final String category;
  final List<MenuItemOption> options;

  MenuItem({
    required this.id,
    required this.itemId,
    required this.name,
    required this.slug,
    required this.tags,
    required this.description,
    required this.imageUrl,
    required this.price,
    required this.inStock,
    required this.category,
    required this.options,
  });

  factory MenuItem.fromJson(Map<String, dynamic> json) {
    var itemIdList = List<int>.from(json['item_id']['data']);
    var tagList = List<String>.from(json['tags']);
    var optionList = (json['options'] as List)
        .map((i) => MenuItemOption.fromJson(i))
        .toList();

    return MenuItem(
      id: json['_id'],
      itemId: itemIdList,
      name: json['name'],
      slug: json['slug'],
      tags: tagList,
      description: json['description'],
      imageUrl: json['image_url'],
      price: double.parse(json['price']['\$numberDecimal']),
      inStock: json['in_stock'],
      category: json['category'],
      options: optionList,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      '_id': id,
      'item_id': {
        'type': 'Buffer',
        'data': itemId,
      },
      'name': name,
      'slug': slug,
      'tags': tags,
      'description': description,
      'image_url': imageUrl,
      'price': {'\$numberDecimal': price.toString()},
      'in_stock': inStock,
      'category': category,
      'options': options.map((option) => option.toJson()).toList(),
    };
  }
}

class MenuItemOption {
  final String id;
  final String type;
  final String value;
  final double fee;

  MenuItemOption({
    required this.id,
    required this.type,
    required this.value,
    required this.fee,
  });

  factory MenuItemOption.fromJson(Map<String, dynamic> json) {
    return MenuItemOption(
      id: json['_id'],
      type: json['type'],
      value: json['value'],
      fee: double.parse(json['fee']['\$numberDecimal']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      '_id': id,
      'type': type,
      'value': value,
      'fee': {'\$numberDecimal': fee.toString()},
    };
  }
}
