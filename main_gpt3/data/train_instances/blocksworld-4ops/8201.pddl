

(define (problem BW-rand-8)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b4)
(on-table b3)
(on-table b4)
(on b5 b1)
(on b6 b7)
(on b7 b5)
(on-table b8)
(clear b3)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b5)
(on b5 b3)
(on b7 b1)
(on b8 b7))
)
)


