import React, { useState } from 'react';
import { View, ImageBackground, Image, TextInput, Button, Text, StyleSheet } from 'react-native';
import { NavigationContainer, useNavigation } from '@react-navigation/native';
import { Alert } from 'react-native';

const LoginScreen = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  // const navigation = useNavigation();

  const handleLogin = () => {
    if (username === 'mina' && password === 'wese5') {
      navigation.navigate('Dashboard');
    } else {
      Alert.alert('Login Failed', 'Please check your username and password.');
    }
  };

  return (
    <NavigationContainer>
        <ImageBackground source={require('./Assets/thumb-1920-638841.png')} style={styles.backgroundImage}>
        <View style={styles.container}>
          <Text style={styles.companyName}>Patient See</Text>
          <Image source={require('./Assets/medical-team.png')} style={styles.logo} />

          <TextInput
            style={styles.input}
            placeholder="Username"
            onChangeText={(text) => console.log('Username:', text)}
          />

          <TextInput
            style={styles.input}
            placeholder="Password"
            secureTextEntry
            onChangeText={(text) => console.log('Password:', text)}
          />

          <Button
            title="Login"
            onPress={() => {
              // Handle the login logic here
            }}
          />
        </View>
      </ImageBackground>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  backgroundImage: {
    flex: 1,
    resizeMode: 'stretch', 
  },
  container: {
    flex: 1,
    justifyContent: 'flex-start', 
    alignItems: 'center',
    paddingTop: 100, 
    backgroundColor: 'rgba(150, 20, 200, 0.4)', 
  },
  companyName: {
    fontSize: 40,
    fontFamily: 'sans-serif',
    fontWeight: 'bold',
    marginBottom: 10,
  },
  logo: {
    width: 200, 
    height: 200,
    marginBottom: 20,
  },
  input: {
    width: 300,
    height: 40,
    borderWidth: 1,
    borderColor: 'cyan',
    borderRadius: 5,
    paddingLeft: 10,
    marginBottom: 10,
    backgroundColor: 'white', 
  },
});


export default LoginScreen;
