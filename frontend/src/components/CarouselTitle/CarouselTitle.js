import React from 'react';

import {motion, AnimatePresence} from "framer-motion";
import styled from 'styled-components';


const AnimatedTitle = styled.div`
  margin-bottom: 1rem ;

  & h1 {
    display: flex;
    color: #212121;
    margin: 0 0.25rem;
  }
`

const TitleWrapper = styled.span`
  display: flex ;
  flex-wrap: wrap;
  & h1 {
    font-size: 1.75rem !important;
    font-weight: unset !important;
    margin-block-end: inherit !important;
  }
`

const AnimatedCarouselTitle = styled.span`
  position: relative !important;
  display: flex;
  justify-content: center ;
  width: 150px;
  margin: 0 15px ;
  white-space: nowrap;

  & .underline {
    width: 170px;
    height: 2px;
    border-radius: 4px;
    position: absolute;
    bottom: -4px;
    left: -10px;
    background: dodgerblue;
  }
  
  & h1 {
    color: #212121 !important;
  }
`

const transitionDuration = 0.4;
const transitionEase = [0.68, -0.55, 0.265, 1.55];
const statement = `For busy people whe need their`;

export default function CarouselTitle({items, current}) {
    return (
        <AnimatedTitle>
                <TitleWrapper>
                    {statement.split(' ').map((word, idx) => (
                        <h1 key={idx}>{word}</h1>
                    ))}
                    <AnimatePresence mode="wait">
                        <AnimatedCarouselTitle>
                            {items.map((item, idx) => {
                                return (
                                    current === idx && (
                                        <React.Fragment key={idx}>
                                            <motion.h1
                                                key={idx}
                                                initial="top"
                                                animate="present"
                                                exit="bottom"
                                                variants={{
                                                    top: {opacity: 0, y: -150},
                                                    present: {opacity: 1, y: 0},
                                                    bottom: {opacity: 0, y: 150},
                                                }}
                                                transition={{duration: transitionDuration, ease: transitionEase}}
                                            >
                                                {item.label}
                                            </motion.h1>
                                        </React.Fragment>
                                    )
                                )
                            })}
                            <div className="underline"/>
                        </AnimatedCarouselTitle>
                    </AnimatePresence>
                    <h1>cleaned.</h1>
                </TitleWrapper>
        </AnimatedTitle>
    )
}