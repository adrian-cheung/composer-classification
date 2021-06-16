import React, { Component, useState, useRef } from 'react';
import {
  Text,
  View,
  Image,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Dimensions,
  ScrollView,
} from 'react-native';
// import DocumentPicker from 'react-native-document-picker';
import * as DocumentPicker from 'expo-document-picker';

let dH = Dimensions.get('window').height;
let dW = Dimensions.get('window').width;

const App = () => {

  const composerImages = {
    'Debussy': 'https://serenademagazine.com/wp-content/uploads/2020/04/Claude_Debussy_atelier_Nadar.jpg',
    'Liszt': 'https://upload.wikimedia.org/wikipedia/commons/6/69/Liszt-kaulbach.jpg',
    'Schubert': 'https://www.wrti.org/sites/wrti/files/201801/schubert.jpg',
    'Chopin': 'https://www.biography.com/.image/t_share/MTc5ODc1MzEwMTk0NDAzMzE3/frederic-francois-chopin-two-to-three-years-before-his-death-in-1849-photo-by-time-life-picturesmansellthe-life-picture-collection-via-getty-images.jpg',
    'Bach': 'https://www.classicsforkids.com/images/composers/Bach.jpg',
    'Haydn': 'https://upload.wikimedia.org/wikipedia/commons/0/05/Joseph_Haydn.jpg',
    'Beethoven': 'https://www.biography.com/.image/t_share/MTI2NTgyMzIxOTcyMjU5NDU5/beethoven-600x600jpg.jpg',
    'Schumann': 'https://media.npr.org/assets/music/artists/robert_schumann-561e710cc3a4ed11ab9eb6fc76214feb7e1c8516-s800-c85.jpg',
    'Rachmaninoff': 'https://pbs.twimg.com/media/D3EWy18UYAIdVab.jpg:large',
    'Mozart': 'https://www.biography.com/.image/t_share/MTE1ODA0OTcxNzMyNjY1ODY5/wolfgang-mozart-9417115-2-402.jpg',
  }

  const [fileUri, setFileUri] = useState('or enter file path here');
  const [predLoadText, setPredLoadText] = useState('PREDICT');
  const [results, setResults] = useState({ '': '', '': '' });

  const scroller = useRef();

  const selectFile = async () => {
    let result = await DocumentPicker.getDocumentAsync({type: 'audio/*', copyToCacheDirectory: false});
    if (result.type === 'success') {
      setFileUri(result.uri);
    }
  };

  const predict = async () => {

    const root = 'U:/My Drive/Classroom/11th Grade/2A - CS Jr Research/CS Jr Research/Labs/Composer Classification/maestro-8000/';

    // POST
    fetch(new URL('/predict', 'http://192.168.1.237:5000'), {
      headers: {
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify({ 'uri': root + fileUri })
    })
      .then(res => res.json())
      .then((res) => {
        setResults(res);
        scroller.current.scrollTo({ y: dH });
      });
  }



  return (
    <View style={styles.container}>
      <ScrollView
        style={styles.scrollContainer}
        scrollEnabled={false}
        ref={scroller}
      >
        <View style={styles.homeScreen}>
          <View style={styles.titleContainer}>
            <Text style={styles.title}>Composer Classification</Text>
          </View>
          <View style={styles.selectFileContainer}>
            <TouchableOpacity onPress={selectFile}>
              <View style={styles.selectFileButton}>
                <Text style={styles.selectFileButtonText}>SELECT FILE</Text>
              </View>
            </TouchableOpacity>
            <TextInput style={styles.selectFileInput}
              onFocus={() => fileUri === 'or enter file path here' && setFileUri('')}
              onChangeText={input => setFileUri(input)}
              value={fileUri}
            />
          </View>
          <TouchableOpacity
            onPress={() => {
              // this.scroller.setNativeProps({ scrollEnabled: false });
              setPredLoadText('LOADING...')
              predict();
            }}>
            <View style={styles.predictButton}>
              <Text style={styles.predictButtonText}>{predLoadText}</Text>
            </View>
          </TouchableOpacity>
        </View>

        <View style={styles.resultsScreen}>
          <View style={styles.resultsContainer}>
            <View style={styles.composerImageContainer}>
              <Image
                source={{ uri: composerImages[Object.keys(results)[0]] }}
                style={styles.composerImage}
              />
            </View>
          </View>
          <View style={styles.predictionsContainer}>
            <View style={styles.composersContainer}>
              <Text style={styles.topPredText}>{Object.keys(results)[0]}</Text>
              {Object.keys(results).slice(1, 5).map((composer) => (
                <Text style={styles.altPredText}>{composer}</Text>
              ))}
            </View>
            <View style={styles.confidencesContainer}>
              <Text style={styles.topPredText}>{Object.values(results)[0]}%</Text>
              {Object.values(results).slice(1, 5).map((confidence) => (
                <Text style={styles.altPredText}>{confidence}%</Text>
              ))}
            </View>
          </View>

          <TouchableOpacity
            onPress={() => {
              setPredLoadText('PREDICT');
              scroller.current.scrollTo({});
            }}>
            <View style={styles.tryAgainButton}>
              <Text style={styles.selectFileButtonText}>TRY AGAIN</Text>
            </View>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    borderWidth: 1,
    borderColor: 'black',
  },
  scrollContainer: {
    height: dH,
    padding: dW / 20,
  },
  homeScreen: {
    width: '100%',
    height: dH - dW / 20,
  },
  resultsScreen: {
    width: '100%',
    height: dH - dW / 20,
    justifyContent: 'center',
  },
  titleContainer: {
    width: '100%',
    height: dH * (2 / 5),
    justifyContent: 'flex-end',
    marginBottom: dW / 20,
  },
  selectFileContainer: {
    width: '100%',
    height: dH * (3/24),
    alignItems: 'stretch',
    justifyContent: 'center',
    borderRadius: dH / 24,
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 6,
    },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    marginBottom: dW / 20,
  },
  selectFileButton: {
    height: dH / 12,
    alignItems: 'center',
    justifyContent: 'center',
    borderTopLeftRadius: dH / 24,
    borderTopRightRadius: dH / 24,
    // borderColor: 'black',
    // borderBottomColor: '#CCCCCC',
    // borderBottomWidth: 2,
    // marginTop: dH/50,
    // marginBottom: dW / 40,
  },
  selectFileInput: {
    // width: '100%',
    height: dH / 24,
    backgroundColor: '#F0F0F0',
    color: 'grey',
    textAlign: 'center',
    fontSize: dH / 48,
    fontFamily: 'Roboto',
    fontStyle: 'italic',
    justifyContent: 'center',
    borderBottomLeftRadius: dH / 24,
    borderBottomRightRadius: dH / 24,
    // borderColor: 'black',
    // borderWidth: 2,
    // borderTopWidth: 0,
    // marginBottom: dW / 40,
  },
  predictButton: {
    width: '100%',
    height: dH / 12,
    backgroundColor: 'black',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: dH / 24,
    // borderColor: 'gray',
    // borderWidth: 1,
    // marginTop: dH/50,
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 6,
    },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    marginBottom: dW / 40,
  },
  title: {
    color: 'black',
    fontSize: dH / 16,
    fontFamily: 'Roboto',
    fontWeight: 'bold',
  },
  selectFileButtonText: {
    color: 'black',
    fontSize: dH / 36,
    fontFamily: 'Roboto',
  },
  predictButtonText: {
    color: 'white',
    fontSize: dH / 36,
    fontFamily: 'Roboto',
  },
  predictionsContainer: {
    width: '100%',
    height: dH / 4,
    flexDirection: 'row',
    justifyContent: 'center',
    marginBottom: dH / 10,
    // borderWidth: 1,
    // borderColor: 'black',
  },
  composerImageContainer: {
    width: '100%',
    height: dH / 3,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: dW / 10,
    // borderWidth: 1,
    // borderColor: 'black',
  },
  composerImage: {
    width: dH / 3,
    height: dH / 3,
    borderRadius: dH / 24,
    overflow: 'hidden',

    borderWidth: 2,
    borderColor: 'black',
  },
  composersContainer: {
    // width: '48%',
    height: '100%',
    // flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    alignSelf: 'flex-start',
    // marginBottom: dW / 40,
    marginRight: dW / 20,
    // borderWidth: 1,
    // borderColor: 'black',
  },
  confidencesContainer: {
    // width: '48%',
    height: '100%',
    // flexDirection: 'row',
    justifyContent: 'space-between',
    alignSelf: 'flex-start',
    // borderWidth: 1,
    // borderColor: 'black',
  },
  topPredText: {
    color: 'black',
    fontSize: dH / 24,
    fontFamily: 'Roboto',
    fontWeight: 'bold',
  },
  altPredText: {
    color: 'black',
    fontSize: dH / 36,
    fontFamily: 'Roboto',
  },
  tryAgainButton: {
    width: '100%',
    height: dH / 12,
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: dH / 24,
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 6,
    },
    shadowOpacity: 0.4,
    shadowRadius: 12,
  },
});

export default App;