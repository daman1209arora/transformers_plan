

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on b1 b4)
(on-table b2)
(on b3 b7)
(on-table b4)
(on b5 b6)
(on b6 b1)
(on-table b7)
(clear b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b2 b5)
(on b3 b2)
(on b5 b4)
(on b6 b3))
)
)

