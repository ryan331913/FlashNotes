import { toaster } from '@/components/ui/toaster'
import { MAX_CHARACTERS } from '@/utils/text'
import type { Editor } from '@tiptap/react'
import { useCallback, useEffect } from 'react'

function useTextCounter(editor: Editor | null, setTextLength: (length: number) => void) {
  const handleTextChange = useCallback(
    (currentEditor: Editor) => {
      if (currentEditor) {
        const currentText = currentEditor.getText()
        setTextLength(currentText.length)
        if (currentText.length > MAX_CHARACTERS) {
          currentEditor.chain().undo().run()
          toaster.create({
            title: 'Characters limitation',
            description: 'Exceed the maximum characters',
            type: 'info',
          })
        }
      }
    },
    [setTextLength],
  )

  useEffect(() => {
    if (editor) {
      const handleUpdate = ({ editor: currentEditor }: { editor: Editor }) => {
        handleTextChange(currentEditor)
      }
      editor.on('update', handleUpdate)
      // Calculate when initialization
      handleTextChange(editor)

      return () => {
        editor.off('update', handleUpdate)
      }
    }
  }, [editor, handleTextChange])

  return
}

export default useTextCounter
