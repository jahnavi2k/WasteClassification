import 'dart:io';
import 'package:camera/camera.dart';
import 'dart:convert' as convert;
import 'dart:convert' show json, utf8;
import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/foundation.dart';
import 'dart:async';
import 'package:http/http.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'package:http/http.dart' as http;

Future<void> main() async {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Home(),
    );
  }
}

class Home extends StatefulWidget {
  @override
  _HomeState createState() => _HomeState();
}

class _HomeState extends State<Home> {
  List<CameraDescription>? cameras; //list out the camera available
  CameraController? controller; //controller for camera
  XFile? image; //for captured image

  @override
  void initState() {
    loadCamera();
    super.initState();
  }

  loadCamera() async {
    cameras = await availableCameras();
    if (cameras != null) {
      controller = CameraController(cameras![0], ResolutionPreset.max);
      //cameras[0] = first camera, change to 1 to another camera

      controller!.initialize().then((_) {
        if (!mounted) {
          return;
        }
        setState(() {});
      });
    } else {
      print("NO any camera found");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Capture Image from Camera"),
        backgroundColor: Colors.redAccent,
      ),
      body: Container(
          child: Column(children: [
        Container(
            height: 300,
            width: 400,
            child: controller == null
                ? Center(child: Text("Loading Camera..."))
                : !controller!.value.isInitialized
                    ? Center(
                        child: CircularProgressIndicator(),
                      )
                    : CameraPreview(controller!)),
        ElevatedButton.icon(
          //image capture button
          onPressed: () async {
            try {
              if (controller != null) {
                //check if controller is not null
                if (controller!.value.isInitialized) {
                  //check if controller is initialized
                  image = await controller!.takePicture(); //capture image
                  print("hello");
                  print(Image.file(new File(image!.path)));
                  setState(() {
                    //update UI
                  });
                }
              }
            } catch (e) {
              print(e); //show error
            }
          },
          icon: Icon(Icons.camera),
          label: Text("Capture"),
        ),
        ElevatedButton.icon(
            //image upload button
            onPressed: () {
              uploadImage('image', File(image!.path));
            },
            icon: Icon(Icons.upload),
            label: Text("Upload")),
        Container(
          //show captured image
          padding: EdgeInsets.all(30),
          child: image == null
              ? Text("No image captured")
              : Image.file(
                  File(image!.path),
                  height: 100,
                ),
          //display captured image
        )
      ])),
    );
  }
}

uploadImage(String title, File file) async {
  var request = http.MultipartRequest(
      "POST", Uri.parse("http://10.0.2.2:8000/file/upload/"));
  request.fields['remark'] = "dummyImage";
  Client client = http.Client();

  var picture = http.MultipartFile.fromBytes('photo', file.readAsBytesSync(),
      filename: 'testimage.png');
  request.files.add(picture);
  var response = await request.send();

  // var response1 = json.decode(
  //     (await client.post(Uri.parse("http://10.0.2.2:8000/file/upload/"))).body);

  // if (response.statusCode == 200) {
  //   // String path = (await getExternalStorageDirectory()).path;
  //   File image = File('assets/specimen.jpg');
  //   await image.writeAsBytes(utf8.encode(response1.data));
  //   // setState(() {});
  // }
  // var response1 =
  //     await http.get(Uri.parse("http://10.0.2.2:8000/file/upload/"));

  // print(response1);
  // List<dynamic> list = convert.jsonDecode(response1.body);
  // print(list);
  var responseData = await response.stream.toBytes();
  var result = String.fromCharCodes(responseData);
  print(result);
  // print("hi");
}
