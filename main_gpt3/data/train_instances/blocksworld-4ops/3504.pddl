

(define (problem BW-rand-7)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b5)
(on-table b3)
(on b4 b7)
(on b5 b3)
(on-table b6)
(on b7 b2)
(clear b1)
(clear b4)
)
(:goal
(and
(on b2 b1)
(on b3 b5)
(on b4 b6)
(on b5 b2))
)
)


