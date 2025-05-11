import { MAX_CHARACTERS } from '@/utils/text'
import { Text } from '@chakra-ui/react'

interface TextCounterProps {
  textLength: number
}

const getTextColor = (currentLength: number) => {
  const percentage = currentLength / MAX_CHARACTERS
  if (percentage > 0.9) {
    return 'red.500'
  }
  return 'gray.500'
}

function TextCounter({ textLength }: TextCounterProps) {
  return (
    <Text position="absolute" bottom="2" right="2" fontSize="sm" color={getTextColor(textLength)}>
      {textLength}/{MAX_CHARACTERS}
    </Text>
  )
}

export default TextCounter
