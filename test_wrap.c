/*
 * test_wrap.c
 *
 *  Created on: Sep 22, 2026
 *      Author: geeta
 */

#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define MAX_LINE_LENGTH 32
#define BUFFER_SIZE 200
#define WORD_SIZE 50

int main(void)
{
    char input[] = "Hello this is a test message to see how the word wrapping works and I just want to say that I'm so happy that this is almost over";

    uint8_t buffer[BUFFER_SIZE];
    uint8_t index = 0;

    char word[WORD_SIZE];
    uint8_t word_index = 0;

    uint8_t current_line = 0;

    for (int i = 0; input[i] != '\0'; i++)
    {
        char byte = input[i];

        /*
         * if byte is part of a word
         */
        if (byte != ' ')
        {
            
            // build the word
            word[word_index++] = byte;
        }
        else
        {
            /*
             * We reached the end of a word
             */
            
            word[word_index] = '\0';

            
            
            /*
             * YOUR WRAPPING LOGIC GOES HERE
             */
            if (word_index + current_line > MAX_LINE_LENGTH) {
                buffer[index++] = '\r';
                buffer[index++] = '\n';
                
                current_line = 0;
            } else {
                if (current_line > 0)
                {
                    buffer[index++] = byte;
                    current_line++;
                }
            }
            for (int i = 0; i < word_index; i++) {
                buffer[index++] = word[i];
                current_line++;
            }

            /*
             * Reset word for the next word
             */
            word_index = 0;

        }
        
    }

    word[word_index] = '\0';

    /*
     * Print the result
     */
    buffer[index] = '\0';

    return 0;
}