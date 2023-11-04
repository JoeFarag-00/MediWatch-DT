import React from 'react';
import { View, Text, ScrollView, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';

const getStatusTextStyle = (status) => {
  let textStyle = styles.text; // Default style

  if (status === 'Awake') {
    textStyle = [styles.text, styles.greenText];
  } else if (status === 'Help') {
    textStyle = [styles.text, styles.orangeText];
  } else if (status === 'Emergency') {
    textStyle = [styles.text, styles.redText];
  }

  return textStyle;
};

const DashboardScreen = () => {
  // const navigation = useNavigation(); // Get the navigation prop

  const navigateToProfile = () => {
    // Handle navigation to the nurse's profile page
    // You can implement the navigation logic here
    // For example: navigation.navigate('NurseProfile');
  };

  const navigateToDashboard = () => {
    // Handle navigation to the default dashboard (patients view)
    // You can implement the navigation logic here
    // For example: navigation.navigate('Dashboard');
  };

  const navigateToNotifications = () => {
    // Handle navigation to the notifications area
    // You can implement the navigation logic here
    // For example: navigation.navigate('Notifications');
  };

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.contentContainer}>
        {/* Profile Cards */}
        <View style={styles.card}>
          <Image source={require('./Assets/people/me.jpg')} style={styles.profileImage} />
          <Text style={styles.text}>Name: Manyoon</Text>
          <Text style={styles.text}>Age: 21</Text>
          <Text style={styles.text}>Room Number: G103A</Text>
          <Text style={styles.text}>Disease/Disability: Wese5</Text>
          <Text style={getStatusTextStyle('Emergency')}>Status: Dead</Text>
        </View>

        <View style={styles.card}>
          <Image source={require('./Assets/people/manyoon.jpg')} style={styles.profileImage} />
          <Text style={styles.text}>Name: King Joe</Text>
          <Text style={styles.text}>Age: 20</Text>
          <Text style={styles.text}>Room Number: D101</Text>
          <Text style={styles.text}>Disease/Disability: Success</Text>
          <Text style={getStatusTextStyle('Awake')}>Status: King</Text>
        </View>

        <View style={styles.card}>
          <Image source={require('./Assets/people/bedan.jpg')} style={styles.profileImage} />
          <Text style={styles.text}>Name: Marzouki</Text>
          <Text style={styles.text}>Age: 20</Text>
          <Text style={styles.text}>Room Number: G408</Text>
          <Text style={styles.text}>Disease/Disability: Bedanphobia</Text>
          <Text style={getStatusTextStyle('Help')}>Status: Help</Text>
        </View>

        {/* Add more profile cards as needed */}
      </ScrollView>

      {/* Taskbar with Buttons */}
      <View style={styles.taskbar}>
        <TouchableOpacity onPress={navigateToProfile}>
          <Image source={require('./Assets/user.png')} style={styles.taskbarButton} />
        </TouchableOpacity>
        <TouchableOpacity onPress={navigateToDashboard}>
          <Image source={require('./Assets/home.png')} style={styles.taskbarButton} />
        </TouchableOpacity>
        <TouchableOpacity onPress={navigateToNotifications}>
          <Image source={require('./Assets/notification.png')} style={styles.taskbarButton} />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  contentContainer: {
    flexGrow: 1,
    alignItems: 'center',
  },
  card: {
    width: 300,
    backgroundColor: 'lightblue',
    padding: 20,
    margin: 10,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 2,
    elevation: 5,
  },
  profileImage: {
    width: 80,
    height: 80,
    borderRadius: 40,
    alignSelf: 'flex-start',
  },
  text: {
    fontSize: 16,
    color: 'black',
    marginVertical: 5,
  },
  greenText: {
    color: 'green',
    fontWeight: 'bold',
  },
  orangeText: {
    color: 'orange',
    fontWeight: 'bold',
  },
  redText: {
    color: 'red',
    fontWeight: 'bold',
  },
  taskbar: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    backgroundColor: 'white',
    padding: 10,
  },
  taskbarButton: {
    width: 30,
    height: 30,
  },
});

export default DashboardScreen;
