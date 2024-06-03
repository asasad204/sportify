"use client";

import '@/app/globals.css';
import { useState } from 'react';
import { Container } from "@/components/Containers/ContainerStyled";
import ParForm from "@/components/Forms/ParForm";
import ProgressIndicator from '@/components/Indicators/ProgressIndicator';
import styled from 'styled-components';
import {Button} from '@/components/Button/ButtonStyled';
import axios from "axios";
import {lapisLazuli} from "@/styles/GlobalStyle";

const Message = styled.h1`
  color: white;
  font-size: 32px;
  text-align: center;
  margin-top: 2rem;
`;

async function sendLostDetails(lostDetails) {
  try {
    const response = await axios.post('http://localhost:8000/lost_and_found', lostDetails);
    return response.data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}

export default function Home() {
  const labelSets = [
    {
      first: {
        label: "tag:lost/found",
        id: "id1",
        name: "tag",
      },
      second: {
        label: "kratki opis",
        id: "id2",
        name: "opis",
      }
    },
    {
      first: {
        label: "lokacija terena",
        id: "id1",
        name: "lokacija",
      },
      second: {
        label: "slika",
        id: "id2",
        name: "slika",
      }
    }
  ];

  const [formKey, setFormKey] = useState(0);
  const [currentLabelSetIndex, setCurrentLabelSetIndex] = useState(0);
  const [formSubmitCount, setFormSubmitCount] = useState(0);
  const [formValues, setFormValues] = useState([]);

  const handlePress = () => {
    let lokacija = parseInt(document.getElementById('id1').value);
    let slika = parseInt(document.getElementById('id2').value);
    const formData = {
      tag: formValues[0],
      opis: formValues[1],
      lokacija: lokacija,
      slika: slika,
    };console.log(formData)

    try {
      axios.post('http://localhost:8000/lost_and_found', formData)
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
       sendLostDetails(formData);
    } catch (error) {
      console.error('Failed to submit form', error);
    }

    setFormSubmitCount((prevCount) => prevCount + 1);
  };

  const NextSlide = () => {
    let prvaVrijednost= document.getElementById("id1").value;
    let drugaVrijednost= document.getElementById("id2").value;
    setFormValues([...formValues,prvaVrijednost,drugaVrijednost])
    if (formSubmitCount < 1) {
      setFormKey((prevKey) => prevKey + 1);
      setCurrentLabelSetIndex((prevIndex) => (prevIndex + 1) % labelSets.length);
      setFormSubmitCount((prevCount) => prevCount + 1);
    } else {
      setFormSubmitCount((prevCount) => prevCount + 1);
    }
  }


  return (
    <Container>
      {formSubmitCount < 2 ? (
        <>
          <ProgressIndicator steps={2} active_number={formSubmitCount + 1} />
          <ParForm
            key={formKey}
            inputs={labelSets[currentLabelSetIndex]}
            h_text={"Osnovne informacije o izgubljenom predmetu"}
          >{(formSubmitCount===1)?(<Button onClick={handlePress}>Završite</Button>) : (<Button onClick={NextSlide}>sljedeće</Button>)}</ParForm>
        </>
      ) : (
        <Message>uspješno ste dodali izgubljeni/pronadjeni predmet</Message>
      )
      }
    </Container>
  );
}