

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on b1 b3)
(on b2 b1)
(on-table b3)
(on b4 b6)
(on-table b5)
(on b6 b2)
(on b7 b4)
(clear b5)
(clear b7)
)
(:goal
(and
(on b3 b2)
(on b4 b7)
(on b6 b5)
(on b7 b6))
)
)

